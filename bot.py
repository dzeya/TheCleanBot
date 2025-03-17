from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os
import logging
from utils.environment import load_environment

# Load environment variables based on environment
env = load_environment()

# Configure logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
logger.info(f"Running in {env} environment with token: {TOKEN[:4]}...{TOKEN[-4:] if TOKEN else 'None'}")

# Build the application (bot) - Set it up for webhook mode
application = ApplicationBuilder().token(TOKEN).build()

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me some text or a photo, and I'll respond with a message.")

# Message handlers
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received text message: {update.message.text}")
    user_text = update.message.text
    # Here you could process the text as needed
    await update.message.reply_text(f"You said: {user_text}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received photo")
    # Telegram sends a list of photo sizes; usually the last one is the largest
    photo = update.message.photo[-1]
    file_id = photo.file_id
    # Download or pass the file_id to an external service, etc.
    # For now, we'll just respond with a text:
    await update.message.reply_text("You sent a photo! (In future, we'll analyze it and return data.)")

# Error handler
async def error_handler(update, context):
    logger.error(f"Update {update} caused error {context.error}")

# Register handlers
application.add_handler(CommandHandler("start", start_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
application.add_error_handler(error_handler)

# Run the bot (polling mode - for local development)
if __name__ == "__main__":
    print("Starting bot...")
    application.run_polling() 