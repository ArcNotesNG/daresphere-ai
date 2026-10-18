import os, logging, asyncio, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "DareSphere AI is LIVE! With God, All Things Are Possible! GOD DID!"

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("DARE_TOKEN") or os.getenv("TELEGRAM_TOKEN") or os.getenv("BOT_TOKEN") or os.getenv("TOKEN")

if not BOT_TOKEN:
    raise ValueError("Add DARE_TOKEN in Render Environment!")

BRAND = "DareSphere AI"
OWNER = "Dare Samuel Olusegun"
LOVE = "Inemisit Dare"
TAGLINE = "With God, All Things Are Possible"

WELCOME_TEXT = f"""
✨ Welcome to DareSphere AI! ✨
Built with love by Dare Samuel Olusegun
💖 Dedicated to My Love - Inemisit Dare
🙏 {TAGLINE}
Ready to serve you with 35 Powers! 🚀
"""

KEYBOARD = [[InlineKeyboardButton("🔥 35 Powers", callback_data="powers")],
            [InlineKeyboardButton("💖 My Love", callback_data="love")]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=InlineKeyboardMarkup(KEYBOARD))

async def powers_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 35 POWERS Active! Chat, Business, CV, Bible, Love & More! Type anything!")

async def love_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💖 For {LOVE} - Forever yours - Dare 💖 ({TAGLINE})")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "powers":
        await q.message.reply_text("💖 For GLOWED - My Everything ❤️ - 35 Powers Ready!")
    else:
        await q.message.reply_text("💖 My Love - Inemisit Dare - Forever!")

async def chat_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"{BRAND}: You said: {update.message.text} - {TAGLINE} 🙏")

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print("DareSphere Bot Starting...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("powers", powers_cmd))
    app.add_handler(CommandHandler("love", love_cmd))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_all))
    print("DareSphere Polling LIVE...")
    app.run_polling(close_loop=False)

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
