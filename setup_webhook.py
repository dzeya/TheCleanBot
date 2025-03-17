import requests
import os
import argparse
import sys
from utils.environment import load_environment

def verify_webhook_endpoint(webhook_url):
    """Verify that the webhook endpoint is accessible"""
    try:
        print(f"Verifying webhook endpoint: {webhook_url}")
        response = requests.get(webhook_url)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:500]}")  # First 500 chars to avoid very long responses
        
        if response.status_code == 200:
            print("✅ Webhook endpoint is accessible")
            return True
        else:
            print(f"❌ Webhook endpoint returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing webhook endpoint: {e}")
        return False

def setup_webhook(environment="production"):
    """Set up the webhook for the specified environment"""
    # Set environment variable before loading
    os.environ["ENVIRONMENT"] = environment
    
    # Load environment variables based on environment
    env = load_environment()
    
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    
    if not TOKEN or not WEBHOOK_URL:
        print(f"Error: Missing required environment variables for {environment} environment")
        print(f"TOKEN: {'Set' if TOKEN else 'Missing'}")
        print(f"WEBHOOK_URL: {'Set' if WEBHOOK_URL else 'Missing'}")
        return False
    
    print(f"Setting up webhook for {environment} environment")
    print(f"Using Telegram token: {TOKEN[:4]}...{TOKEN[-4:] if TOKEN else 'None'}")
    print(f"Using webhook URL: {WEBHOOK_URL}")
    
    # Verify the webhook endpoint is accessible
    if not verify_webhook_endpoint(WEBHOOK_URL):
        print("Warning: Webhook endpoint verification failed.")
        proceed = input("Do you want to continue with setting up the webhook? (y/n): ")
        if proceed.lower() != 'y':
            print("Aborting webhook setup.")
            return False

    # First, delete any existing webhook
    delete_url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
    delete_response = requests.get(delete_url)
    print(f"Delete webhook response: {delete_response.json()}")
    
    # Now set the new webhook
    set_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    set_response = requests.post(set_url, data={"url": WEBHOOK_URL})
    print(f"Set webhook response: {set_response.json()}")
    
    # Get webhook info
    info_url = f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo"
    info_response = requests.get(info_url)
    print(f"Webhook info: {info_response.json()}")
    
    return True

def main():
    # Setup command line arguments
    parser = argparse.ArgumentParser(description='Set up Telegram bot webhook')
    parser.add_argument('--env', '-e', choices=['development', 'production'], 
                        default='production', help='Environment to use (development or production)')
    parser.add_argument('--verify-only', action='store_true', 
                        help='Only verify the webhook endpoint without setting up')
    
    args = parser.parse_args()
    
    # Set environment variable
    os.environ["ENVIRONMENT"] = args.env
    
    # Load environment variables
    env = load_environment()
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    
    if args.verify_only:
        if WEBHOOK_URL:
            verify_webhook_endpoint(WEBHOOK_URL)
        else:
            print("Error: WEBHOOK_URL is not set in the environment")
    else:
        # Call the setup function with the specified environment
        setup_webhook(args.env)

if __name__ == "__main__":
    main() 