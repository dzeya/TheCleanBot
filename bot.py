from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Build the application (bot)
application = ApplicationBuilder().token(TOKEN).build()

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me some text or a photo, and I'll respond with a message.")

# Message handlers
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Here you could process the text as needed
    await update.message.reply_text(f"You said: {user_text}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Telegram sends a list of photo sizes; usually the last one is the largest
    photo = update.message.photo[-1]
    file_id = photo.file_id
    # Download or pass the file_id to an external service, etc.
    # For now, we'll just respond with a text:
    await update.message.reply_text("You sent a photo! (In future, we'll analyze it and return data.)")

# Register handlers
application.add_handler(CommandHandler("start", start_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

# Run the bot (polling mode - for local development)
if __name__ == "__main__":
    print("Starting bot...")
    application.run_polling() 