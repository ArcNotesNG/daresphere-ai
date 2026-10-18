import os, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("DARE_TOKEN") or os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Add DARE_TOKEN in Render")

BRAND = "DareSphere AI"
OWNER = "Dare Samuel Olusegun"
LOVE = "Inemesit Dare"
TAGLINE = "With God, All Things Are Possible"

WELCOME_TEXT = f"""
🌐 *Welcome to DareSphere AI* ✨
Built with Love by Dare Samuel Olusegun
❤️ Dedicated to My Love — Inemesit Dare
🙏 {TAGLINE}
Ready to serve you with 35 Powers! 🚀
"""

KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("📜 See 35 Powers", callback_data="powers")],
    [InlineKeyboardButton("❤️ My Love", callback_data="mylove")],
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=KEYBOARD, parse_mode="Markdown")

async def powers_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 35 POWERS Active! Chat, Business, CV, Bible... ❤️")

async def love_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"❤️ For {LOVE} — Forever yours — Dare 💙\n🙏 {TAGLINE}")

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "mylove":
        await q.message.reply_text(f"❤️ For {LOVE} — My Everything! 💙")
    else:
        await q.message.reply_text("📜 35 POWERS — Type /start")

async def chat_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🤖 {BRAND}: You said _{update.message.text}_ ❤️", parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("powers", powers_cmd))
    app.add_handler(CommandHandler("mylove", love_cmd))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_all))
    print(f"{BRAND} LIVE...")
    app.run_polling()

if __name__ == "__main__":
    main()
