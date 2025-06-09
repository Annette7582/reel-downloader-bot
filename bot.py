import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from yt_dlp import YoutubeDL
import nest_asyncio

# trigger redeploy

nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8443))
DOMAIN = os.getenv("RAILWAY_PUBLIC_DOMAIN")
INSTAGRAM_COOKIE = os.getenv("INSTAGRAM_COOKIE")

# Write the cookie to a file
with open("cookies.txt", "w") as f:
    f.write(INSTAGRAM_COOKIE)

ydl_opts = {
    'cookiefile': 'cookies.txt',
    'outtmpl': 'downloads/%(title)s.%(ext)s'
}

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👀 Bot zinda hai, message mila!")

app.add_handler(MessageHandler(filters.ALL, echo))

# Save cookie to file
with open("instagram.com_cookies.txt", "w") as f:
    f.write(COOKIE)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me an Instagram Reel link to download.")

async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    print(f"[RECEIVED] Text: {text}")

async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        print("[BOT] Message received:", text)

        if "instagram.com/reel/" not in text:
            await update.message.reply_text("❌ Bhai sahi reel link bhejo.")
            return

# Reel downloader
async def download_reel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com/reel" not in url:
        await update.message.reply_text("❌ Invalid Instagram Reel URL.")
        return

    await update.message.reply_text("⏬ Downloading reel...")

    ydl_opts = {
        'outtmpl': 'reel.%(ext)s',
        'quiet': True,
        'cookiesfromfile': 'instagram.com_cookies.txt',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, 'rb') as f:
            await update.message.reply_video(video=f)

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Failed to download:\n{str(e)}")

# Bot setup
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, download_reel))

app.add_handler(MessageHandler(filters.ALL, echo))

# Webhook
if DOMAIN:
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{DOMAIN}/webhook"
    )
else:
    app.run_polling()
