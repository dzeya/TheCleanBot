import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://the-clean-bot.vercel.app/api/bot-webhook")

def main():
    # First, delete any existing webhook
    delete_url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
    delete_response = requests.get(delete_url)
    print(f"Delete webhook response: {delete_response.json()}")
    
    # Now set the new webhook
    set_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
    set_response = requests.get(set_url)
    print(f"Set webhook response: {set_response.json()}")
    
    # Get webhook info
    info_url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
    info_response = requests.get(info_url)
    print(f"Webhook info: {info_response.json()}")

if __name__ == "__main__":
    main() 