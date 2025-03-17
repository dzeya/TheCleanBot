import requests
from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import logging
import traceback

# Add parent directory to path to import from bot.py and utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.environment import load_environment

# Configure logging first (before anything else)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug: Print current working directory and files
logger.info(f"Current working directory: {os.getcwd()}")
try:
    files = os.listdir(".")
    logger.info(f"Files in current directory: {files}")
    
    # Check for specific env files
    env_files = [f for f in files if f.startswith('.env')]
    logger.info(f"Environment files found: {env_files}")
except Exception as e:
    logger.error(f"Error listing files: {e}")

# Log all environment variables (without sensitive data)
logger.info("Environment variables (excluding sensitive data):")
for key in os.environ:
    if not ("TOKEN" in key or "KEY" in key or "SECRET" in key or "PASSWORD" in key):
        logger.info(f"{key}: {os.environ[key]}")

try:
    # Load environment variables based on environment
    env = load_environment()
    
    # Setup webhook - use the appropriate variables based on environment
    if env == "production":
        TOKEN = os.getenv("TELEGRAM_TOKEN_PROD")
        WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL_PROD", "https://the-clean-bot.vercel.app/api/bot-webhook")
    else:
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL", "https://the-clean-bot-git-develop-dzeyas-projects.vercel.app/api/bot-webhook")
    
    # Log environment and token validation
    logger.info(f"API running in {env} environment")
    logger.info(f"Using webhook URL: {WEBHOOK_URL}")
    if not TOKEN:
        logger.error("TELEGRAM_TOKEN is missing or empty!")
    else:
        logger.info(f"TELEGRAM_TOKEN loaded: {TOKEN[:4]}...{TOKEN[-4:]}")
except Exception as e:
    logger.error(f"Error during initialization: {e}")
    logger.error(traceback.format_exc())
    # Continue with default empty values to avoid crashing the app
    env = "unknown"
    TOKEN = ""
    WEBHOOK_URL = "https://the-clean-bot.vercel.app/api/bot-webhook"

def setup_webhook():
    """Set up the webhook with Telegram."""
    if not TOKEN:
        logger.error("Cannot set up webhook: TOKEN is missing")
        return {"ok": False, "error": "TOKEN is missing"}
        
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
    try:
        response = requests.get(url)
        response_json = response.json()
        logger.info(f"Webhook setup response: {response_json}")
        return response_json
    except Exception as e:
        logger.error(f"Error setting up webhook: {e}")
        logger.error(traceback.format_exc())
        return {"ok": False, "error": str(e)}

def send_telegram_message(chat_id, text):
    """Send a message to Telegram."""
    if not TOKEN:
        logger.error("Cannot send message: TOKEN is missing")
        return {"ok": False, "error": "TOKEN is missing"}
        
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(url, json=data)
        response_json = response.json()
        logger.info(f"Send message response: {response_json}")
        return response_json
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        logger.error(traceback.format_exc())
        return {"ok": False, "error": str(e)}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            logger.info(f"Received POST request to path: {self.path}")
            logger.info(f"Headers: {self.headers}")
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse the update from Telegram
            update = json.loads(post_data.decode('utf-8'))
            logger.info(f"Received update: {update}")
            
            # Process the update directly
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                
                # Process commands
                if 'text' in message:
                    text = message['text']
                    entities = message.get('entities', [])
                    
                    # Check for /start command
                    is_command = False
                    for entity in entities:
                        if entity.get('type') == 'bot_command' and text.startswith('/start'):
                            is_command = True
                            send_telegram_message(chat_id, f"Hello! Send me some text or a photo, and I'll respond with a message. (Running in {env} environment)")
                            break
                    
                    # Handle regular text messages
                    if not is_command and text:
                        send_telegram_message(chat_id, f"You said: {text}")
                
                # Process photos
                if 'photo' in message:
                    send_telegram_message(chat_id, "You sent a photo! (In future, we'll analyze it and return data.)")
            
            # Respond to Telegram with 200 OK
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("OK".encode())
            
        except Exception as e:
            logger.error(f"Error processing update: {e}")
            logger.error(traceback.format_exc())
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())
    
    def do_GET(self):
        try:
            logger.info(f"Received GET request to path: {self.path}")
            
            # Set up webhook and return status
            status = setup_webhook()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": f"Telegram Bot Webhook is running in {env} environment!",
                "webhook_setup": status
            }).encode())
        except Exception as e:
            logger.error(f"Error handling GET request: {e}")
            logger.error(traceback.format_exc())
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode()) 