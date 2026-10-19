import os, threading
from flask import Flask
from groq import Groq
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "DareSphere AI Live!"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = "You are DareSphere AI, built by Dare Samuel Olusegun, dedicated to Inemisit Dare (GLOWED). You are like ChatGPT - intelligent, helpful, friendly. Never repeat slogan unless asked."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["history"] = []
    await update.message.reply_text("Hey Boss! 🔥 I'm DareSphere AI\nBuilt by Dare Samuel Olusegun ❤️\nDedicated to Inemisit Dare (GLOWED)\n\nWith God, All Things Are Possible. GOD DID! 🙏\n\nI can hear VOICE NOTES now! 🎤 Send me a voice!")

async def handle_text(text, update, context):
    if "history" not in context.chat_data:
        context.chat_data["history"] = []
    context.chat_data["history"].append({"role": "user", "content": text})
    history = context.chat_data["history"][-10:]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    try:
        res = client.chat.completions.create(model="openai/gpt-oss-20b", messages=messages, temperature=0.7, max_tokens=800)
        reply = res.choices[0].message.content
        context.chat_data["history"].append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_text(update.message.text, update, context)

async def voice_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎧 Listening to your voice...")
    try:
        vf = await update.message.voice.get_file()
        path = f"/tmp/{vf.file_id}.ogg"
        await vf.download_to_drive(path)
        with open(path, "rb") as f:
            t = client.audio.transcriptions.create(file=(path, f.read()), model="whisper-large-v3")
        text = t.text
        await update.message.reply_text(f"🎤 You said: {text}")
        await handle_text(text, update, context)
        os.remove(path)
    except Exception as e:
        await update.message.reply_text(f"Voice Error: {e}")

async def post_init(app):
    await app.bot.delete_webhook(drop_pending_updates=True)

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.add_handler(MessageHandler(filters.VOICE, voice_chat))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
