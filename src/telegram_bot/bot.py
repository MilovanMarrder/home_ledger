import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from .client import BackendClient

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
API_KEY = os.getenv("BACKEND_API_KEY", "dev-key")

client = BackendClient(BASE_URL, API_KEY)

from datetime import date

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text or ""

    draft = client.send_text(user_id, text)
    await update.message.reply_text(
        f"Borrador #{draft['id']} | status={draft['status']} | kind={draft['kind']} | amount={draft['amount']}"
    )

    # MVP: auto-confirmar si ya hay kind + amount
    if draft.get("kind") and draft.get("amount"):
        kind = draft["kind"]
        today = date.today().isoformat()

        # defaults solo para prueba
        if kind == "expense":
            payload = {
                "kind": "expense",
                "txn_date": today,
                "currency": "HNL",
                "amount": float(draft["amount"]),
                "merchant": draft.get("merchant"),
                "notes": text,
                "category_code": "EXP.FOOD.GROCERY",  # default prueba
            }
        elif kind == "income":
            payload = {
                "kind": "income",
                "txn_date": today,
                "currency": "HNL",
                "amount": float(draft["amount"]),
                "merchant": draft.get("merchant"),
                "notes": text,
                "category_code": "INC.SALARY",  # default prueba
            }
        else:
            await update.message.reply_text("Kind no soportado para auto-confirm en MVP.")
            return

        try:
            posted = client.confirm_draft(draft["id"], payload)
            await update.message.reply_text(
                f"✅ Posteado. txn_id={posted['transaction_id']} | entry_id={posted['journal_entry_id']}"
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error posteando: {e}")
    else:
        await update.message.reply_text("Faltan datos (kind/amount). En MVP todavía no hago preguntas.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    msg = update.message
    tg_file = None
    filename = "upload.bin"
    mime = "application/octet-stream"

    if msg.photo:
        tg_file = await msg.photo[-1].get_file()
        filename = "photo.jpg"
        mime = "image/jpeg"
    elif msg.document:
        tg_file = await msg.document.get_file()
        filename = msg.document.file_name or "document"
        mime = msg.document.mime_type or mime
    elif msg.audio:
        tg_file = await msg.audio.get_file()
        filename = "audio.ogg"
        mime = msg.audio.mime_type or "audio/ogg"
    elif msg.voice:
        tg_file = await msg.voice.get_file()
        filename = "voice.ogg"
        mime = "audio/ogg"

    if not tg_file:
        await msg.reply_text("Tipo de archivo no soportado en MVP.")
        return

    file_bytes = await tg_file.download_as_bytearray()
    draft = client.send_file(user_id, bytes(file_bytes), filename, mime)
    await msg.reply_text(f"Archivo recibido. Borrador #{draft['id']} | status={draft['status']}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.ATTACHMENT, handle_file))
    app.run_polling()

if __name__ == "__main__":
    main()
