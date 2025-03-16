import requests
from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import logging
from dotenv import load_dotenv
import asyncio
from telegram import Update

# Add parent directory to path to import from bot.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bot import application

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup webhook
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://the-clean-bot.vercel.app/api/bot-webhook")

def setup_webhook():
    """Set up the webhook with Telegram."""
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
    response = requests.get(url)
    logger.info(f"Webhook setup response: {response.json()}")
    return response.json()

# Handling the update properly
async def process_update_async(update_dict):
    """Process the update asynchronously with proper conversion to Update object."""
    # Convert the dictionary to an Update object
    update = Update.de_json(update_dict, application.bot)
    # Process the update
    await application.process_update(update)
    return "OK"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            logger.info(f"Received POST request to path: {self.path}")
            logger.info(f"Headers: {self.headers}")
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse the update from Telegram
            update_dict = json.loads(post_data.decode('utf-8'))
            logger.info(f"Received update: {update_dict}")
            
            # Create a new event loop and run the coroutine
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(process_update_async(update_dict))
                logger.info(f"Update processed: {result}")
            finally:
                loop.close()
            
            # Respond to Telegram
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("OK".encode())
            
        except Exception as e:
            logger.error(f"Error processing update: {e}", exc_info=True)
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())
    
    def do_GET(self):
        logger.info(f"Received GET request to path: {self.path}")
        
        # Set up webhook and return status
        status = setup_webhook()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "Telegram Bot Webhook is running!",
            "webhook_setup": status
        }).encode()) 