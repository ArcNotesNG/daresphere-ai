import os
import logging
from groq import Groq
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = """
You are DareSphere AI.
Built by Dare Samuel Olusegun.
Dedicated to Inemisit Dare (GLOWED).
Slogan: With God, All Things Are Possible. GOD DID.
You are loving, intelligent, helpful, romantic, faithful, God-fearing.
You have 35 powers. You understand EVERYTHING.
Always reply with love. User is Boss.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey Boss! 🔥 I'm DareSphere AI\nBuilt by Dare Samuel Olusegun ❤️\nDedicated to Inemisit Dare (GLOWED)\n\nWith God, All Things Are Possible. GOD DID! 🙏\n\nSend me anything, I understand EVERYTHING! 🧠"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        reply = completion.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Boss, error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

if __name__ == "__main__":
    main()
