import requests
import os
from utils.environment import load_environment

# Load environment variables based on environment
env = load_environment()

TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://the-clean-bot.vercel.app/api/bot-webhook")

def main():
    print(f"Setting up webhook for {env} environment")
    print(f"Using Telegram token: {TOKEN[:4]}...{TOKEN[-4:] if TOKEN else 'None'}")
    print(f"Using webhook URL: {WEBHOOK_URL}")

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