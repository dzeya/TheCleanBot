# Telegram Bot Webhook Setup

This document explains how to set up webhooks for your Telegram bot in both development and production environments.

## Environment Setup

The project supports multiple environments:

- **Production**: Uses settings from `.env`
- **Development**: Uses settings from `.env.development`

Each environment file contains the Telegram bot token and webhook URL specific to that environment.

## Environment Files

### Production (`.env`)
```
TELEGRAM_TOKEN=7408476521:AAGQOScYGmoO3mZjN7kyWf0DKya0vv8sc6k
WEBHOOK_URL=https://the-clean-bot.vercel.app/api/bot-webhook
ENVIRONMENT=production
```

### Development (`.env.development`)
```
TELEGRAM_TOKEN=7771484255:AAFZo8gZi3bXJJfCwb5s5MqT35IU19OqCSI
WEBHOOK_URL=https://the-clean-bot-git-develop-dzeyas-projects.vercel.app/api/bot-webhook
ENVIRONMENT=development
```

## Verifying Webhook Endpoints

Before setting up your webhooks, you can verify that the webhook endpoints are accessible:

```bash
# For development environment
python setup_webhook.py --env development --verify-only

# For production environment
python setup_webhook.py --env production --verify-only
```

If the verification fails, it might indicate:
- Your Vercel deployment is not live yet
- The API routes are not properly configured
- There's an issue with the bot-webhook endpoint

## Setting Up Webhooks

### Using the Setup Script

The easiest way to set up your webhooks is to use the provided script:

```bash
# For development environment
python setup_webhook.py --env development

# For production environment (default)
python setup_webhook.py --env production
# or simply
python setup_webhook.py
```

### Manual Setup

If you prefer to set up the webhooks manually, you can use either of these methods:

#### Using cURL

For Development:
```bash
export DEV_TELEGRAM_TOKEN="7771484255:AAFZo8gZi3bXJJfCwb5s5MqT35IU19OqCSI"
export DEV_TELEGRAM_WEBHOOK_URL="https://the-clean-bot-git-develop-dzeyas-projects.vercel.app/api/bot-webhook"

curl -F "url=$DEV_TELEGRAM_WEBHOOK_URL" \
     https://api.telegram.org/bot$DEV_TELEGRAM_TOKEN/setWebhook
```

For Production:
```bash
export PROD_TELEGRAM_TOKEN="7408476521:AAGQOScYGmoO3mZjN7kyWf0DKya0vv8sc6k"
export PROD_TELEGRAM_WEBHOOK_URL="https://the-clean-bot.vercel.app/api/bot-webhook"

curl -F "url=$PROD_TELEGRAM_WEBHOOK_URL" \
     https://api.telegram.org/bot$PROD_TELEGRAM_TOKEN/setWebhook
```

#### Using Python

For Development:
```python
import os, requests

dev_token = os.environ["DEV_TELEGRAM_TOKEN"]
dev_webhook_url = os.environ["DEV_TELEGRAM_WEBHOOK_URL"]
set_webhook_url = f"https://api.telegram.org/bot{dev_token}/setWebhook"
response = requests.post(set_webhook_url, data={"url": dev_webhook_url})
print(response.json())
```

For Production:
```python
import os, requests

prod_token = os.environ["PROD_TELEGRAM_TOKEN"]
prod_webhook_url = os.environ["PROD_TELEGRAM_WEBHOOK_URL"]
set_webhook_url = f"https://api.telegram.org/bot{prod_token}/setWebhook"
response = requests.post(set_webhook_url, data={"url": prod_webhook_url})
print(response.json())
```

## Verifying Webhook Setup

You can verify that your webhook is set up correctly by checking the webhook info:

```bash
# For development
curl https://api.telegram.org/bot$DEV_TELEGRAM_TOKEN/getWebhookInfo

# For production
curl https://api.telegram.org/bot$PROD_TELEGRAM_TOKEN/getWebhookInfo
```

The response should show your webhook URL and confirm that it's active.

## Troubleshooting

If you encounter 404 errors when accessing your webhook URLs:

1. Make sure your Vercel deployment is complete and successful
2. Verify that your `vercel.json` has the correct routes:
   ```json
   {
     "routes": [
       { "src": "/api/bot-webhook", "dest": "api/bot-webhook.py" }
     ]
   }
   ```
3. Check that both `api/webhook.py` and `api/bot-webhook.py` files exist in your project
4. Try accessing the endpoints manually in your browser to see the specific error messages
5. Check Vercel logs for any deployment or runtime errors 