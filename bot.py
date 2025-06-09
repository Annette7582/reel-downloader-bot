from dotenv import load_dotenv
import os
import logging
import asyncio
from telegram import Update
from config import BOT_TOKEN
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
print("BOT TOKEN:", os.getenv("BOT_TOKEN"))
print("IG COOKIE:", os.getenv("IG_COOKIE"))

import yt_dlp

load_dotenv(dotenv_path=".env")

# Get token securely
BOT_TOKEN = os.getenv("BOT_TOKEN")

print(f"[DEBUG] TOKEN: {BOT_TOKEN}")  # Temporary print for log checking

# Enable Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me an Instagram Reel link to download.")


# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)


# Reel downloader logic
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "instagram.com/reel" in text:
        await update.message.reply_text("⬇️ Downloading the Reel...")

        try:
            ydl_opts = {
                'outtmpl': 'reel.%(ext)s',
                'format': 'mp4',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                file_path = ydl.prepare_filename(info)

            await update.message.reply_video(video=open(file_path, 'rb'))

            # Clean up
            os.remove(file_path)

        except Exception as e:
            logger.error(f"Download error: {e}")
            await update.message.reply_text("⚠️ Failed to download. Link may be private or invalid.")

    else:
        await update.message.reply_text("❌ Please send a valid Instagram Reel link.")


# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
