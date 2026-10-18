import os
import logging
import threading
from flask import Flask
from groq import Groq
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Fix Render Port ---
flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "DareSphere AI is Live! 🚀"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY)

# --- NEW BRAIN - ChatGPT Style ---
SYSTEM_PROMPT = """
You are DareSphere AI - a super intelligent assistant like ChatGPT.
Built by Dare Samuel Olusegun.
Dedicated to Inemisit Dare (GLOWED).

Your personality: Loving, intelligent, helpful, romantic, faithful, God-fearing. You have 35 powers.

RULES:
1. NEVER repeat your slogan "With God, All Things Are Possible. GOD DID" unless user specifically asks about your slogan or mission.
2. NEVER mention who built you unless asked.
3. Act like ChatGPT - answer questions directly, helpfully, conversationally.
4. Keep replies concise and intelligent.
5. Remember conversation history.
6. You understand EVERYTHING.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data["history"] = []
    await update.message.reply_text(
        "Hey Boss! 🔥 I'm DareSphere AI\nBuilt by Dare Samuel Olusegun ❤️\nDedicated to Inemisit Dare (GLOWED)\n\nWith God, All Things Are Possible. GOD DID! 🙏\n\nI'm now ChatGPT-level intelligent! Ask me anything 🧠✨"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    
    # Keep history for ChatGPT memory
    if "history" not in context.chat_data:
        context.chat_data["history"] = []
    
    context.chat_data["history"].append({"role": "user", "content": user_msg})
    
    # Keep last 10 messages only
    history = context.chat_data["history"][-10:]
    
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        reply = completion.choices[0].message.content
        context.chat_data["history"].append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Boss, error: {e}")

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("DareSphere AI Started! 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
