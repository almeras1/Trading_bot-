import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, filters, ContextTypes
)
from analyzer import analyze_chart

load_dotenv()
logging.basicConfig(level=logging.INFO)

async def start(update, context):
    await update.message.reply_text(
        "👋 Salut ! Je suis ton assistant trading.\n\n"
        "📸 Envoie-moi un screenshot de ton graphique\n"
        "💬 Tu peux ajouter une question en légende\n\n"
        "Exemple : envoie une image avec 'BUY ou SELL ?'"
    )

async def handle_photo(update, context):
    await update.message.reply_text("🔍 Analyse en cours...")
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_bytes = await file.download_as_bytearray()
    question = update.message.caption or None
    try:
        result = analyze_chart(bytes(image_bytes), question)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur : {str(e)}")

async def handle_text(update, context):
    await update.message.reply_text(
        "📸 Envoie-moi un screenshot de ton graphique !"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
