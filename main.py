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

SYSTEM_PROMPT = "You are DareSphere AI, built by Dare Samuel Olusegun, dedicated to Inemisit Dare (GLOWED). You are like ChatGPT - intelligent, helpful. Never repeat slogan unless asked."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["history"] = []
    await update.message.reply_text("Hey Boss! 🔥 I'm DareSphere AI\nBuilt by Dare Samuel Olusegun ❤️\nDedicated to Inemisit Dare (GLOWED)\n\nWith God, All Things Are Possible. GOD DID! 🙏\n\nAsk me anything!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    if "history" not in context.chat_data:
        context.chat_data["history"] = []
    context.chat_data["history"].append({"role": "user", "content": msg})
    history = context.chat_data["history"][-10:]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    try:
        res = client.chat.completions.create(model="openai/gpt-oss-20b", messages=messages, temperature=0.7, max_tokens=800)
        reply = res.choices[0].message.content
        context.chat_data["history"].append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
