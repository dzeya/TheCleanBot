import requests
import os

# Bot token and webhook URL for the test bot
TEST_BOT_TOKEN = "7771484255:AAFZo8gZi3bXJJfCwb5s5MqT35IU19OqCSI"
NEW_WEBHOOK_URL = "https://the-clean-bot-git-develop-dzeyas-projects.vercel.app/api/bot-webhook"

def reset_webhook():
    # First, delete the current webhook
    delete_url = f"https://api.telegram.org/bot{TEST_BOT_TOKEN}/deleteWebhook"
    delete_response = requests.get(delete_url)
    print(f"Delete webhook response: {delete_response.json()}")
    
    # Wait a moment
    import time
    time.sleep(1)
    
    # Now set the new webhook
    set_url = f"https://api.telegram.org/bot{TEST_BOT_TOKEN}/setWebhook"
    set_response = requests.post(set_url, data={"url": NEW_WEBHOOK_URL})
    print(f"Set webhook response: {set_response.json()}")
    
    # Get webhook info to verify
    info_url = f"https://api.telegram.org/bot{TEST_BOT_TOKEN}/getWebhookInfo"
    info_response = requests.get(info_url)
    print(f"Webhook info: {info_response.json()}")

if __name__ == "__main__":
    print("Resetting webhook for test bot...")
    reset_webhook()
    print("Done!") 