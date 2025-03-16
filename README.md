# TheCleanBot

A Telegram bot that handles text and photo messages.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
- Create a `.env` file with your Telegram Bot Token:
```
TELEGRAM_TOKEN=your_telegram_token
```

## Local Development

Run the bot locally with polling (for development):
```bash
python bot.py
```

## Webhook Deployment on Vercel

1. Deploy to Vercel:
```bash
vercel
```

2. Set the webhook URL in Telegram:
```
https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=<YOUR_VERCEL_URL>
```

## Features

- Responds to the `/start` command
- Handles text messages
- Handles photo messages (with placeholder response)

## Future Enhancements

- Integration with OpenAI for photo analysis
- Database integration with Supabase
- Enhanced UX with inline keyboards 