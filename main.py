import os
import logging
import threading
from flask import Flask
from groq import Groq
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Fix Render Port so it stays Live
flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "DareSphere AI is Live! GOD DID!"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = """
You are DareSphere AI - a super intelligent assistant like ChatGPT.
Built by Dare Samuel Olusegun.
Dedicated to Inemisit Dare (GLOWED).
You are loving, intelligent, helpful.
RULE: Never repeat your slogan or builder info unless user asks. Just answer helpfully like ChatGPT.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["history"] = []
    await update.message.reply_text(
        "Hey Boss! 🔥 I'm DareSphere AI\nBuilt by Dare Samuel Olusegun ❤️\nDedicated to Inemisit Dare (GLOWED)\n\nWith God, All Things Are Possible. GOD DID! 🙏\n\nI'm now ChatGPT-level intelligent! Ask me anything 🧠"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    if "history" not in context.chat_data:
        context.chat_data["history"] = []
    
    context.chat_data["history"].append({"role": "user", "content": user_msg})
    history = context.chat_data["history"][-10:]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
           
