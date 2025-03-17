import requests
from http.server import BaseHTTPRequestHandler
import json
import os
import logging

# Configure simple logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment detection (simplest possible)
ENV = os.getenv("VERCEL_ENV", "development")
if ENV == "production":
    # Production environment
    TOKEN = os.getenv("TELEGRAM_TOKEN_PROD", "")
    WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL_PROD", "https://the-clean-bot.vercel.app/api/bot-webhook")
else:
    # Development/Preview environment
    TOKEN = os.getenv("TELEGRAM_TOKEN", "")
    WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL", "https://the-clean-bot-git-develop-dzeyas-projects.vercel.app/api/bot-webhook")

# Log configuration
logger.info(f"Bot initialized in {ENV} environment")
logger.info(f"Using webhook URL: {WEBHOOK_URL}")
if TOKEN:
    logger.info(f"TOKEN loaded: {TOKEN[:4]}...{TOKEN[-4:] if len(TOKEN) > 8 else ''}")
else:
    logger.error("TOKEN is missing or empty!")

def send_telegram_message(chat_id, text):
    """Send a message via Telegram API."""
    if not TOKEN:
        logger.error("Cannot send message: TOKEN is missing")
        return {"ok": False, "error": "TOKEN is missing"}
        
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return {"ok": False, "error": str(e)}

def setup_webhook():
    """Set up the webhook with Telegram."""
    if not TOKEN:
        logger.error("Cannot set up webhook: TOKEN is missing")
        return {"ok": False, "error": "TOKEN is missing"}
        
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        logger.error(f"Error setting up webhook: {e}")
        return {"ok": False, "error": str(e)}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests from Telegram."""
        try:
            # Log request details
            logger.info(f"Received POST request: {self.path}")
            
            # Read the request body
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                update = json.loads(post_data.decode("utf-8"))
                
                # Process message
                if "message" in update:
                    message = update["message"]
                    chat_id = message["chat"]["id"]
                    
                    # Process text messages
                    if "text" in message:
                        text = message["text"]
                        
                        # Check for /start command
                        if text.startswith("/start"):
                            send_telegram_message(chat_id, f"Hello! I'm running in {ENV} environment. Send me a message and I'll reply.")
                        else:
                            send_telegram_message(chat_id, f"You said: {text}")
                    
                    # Process photo messages
                    elif "photo" in message:
                        send_telegram_message(chat_id, "You sent a photo! (In future, I'll analyze it)")
            
            # Always respond with 200 OK to Telegram
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("OK".encode())
            
        except Exception as e:
            logger.error(f"Error processing update: {e}")
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())
    
    def do_GET(self):
        """Handle GET requests for webhook setup and status checks."""
        try:
            logger.info(f"Received GET request: {self.path}")
            
            # Set up the webhook and return status
            status = setup_webhook()
            response = {
                "status": f"Bot webhook is running in {ENV} environment",
                "webhook": status
            }
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logger.error(f"Error handling GET request: {e}")
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode()) 