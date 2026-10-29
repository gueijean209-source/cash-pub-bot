import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN") # Ton token sera sur Render, pas ici
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot Cash Pub CI en ligne !"

def run_flask():
    app_flask.run(host="0.0.0.0", port=10000)

# --- LOGIQUE DU BOT ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Mon Solde", callback_data='solde')],
        [InlineKeyboardButton("👥 Parrainage", callback_data='parrainage')],
        [InlineKeyboardButton("📞 Support", callback_data='support')]
    ]
    await update.message.reply_text(
        "Bienvenue sur Cash Pub CI 🇨🇮\n\nGagne des bonus en invitant tes amis !\n\nClique sur les boutons ci-dessous :",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'solde':
        await query.edit_message_text("Ton solde : 0 FCFA\nInvite des amis pour gagner !")
    elif query.data == 'parrainage':
        link = f"https://t.me/{context.bot.username}?start={query.from_user.id}"
        await query.edit_message_text(f"Ton lien de parrainage :\n{link}\n\nTu gagnes 100F par ami invité.")
    elif query.data == 'support':
        await query.edit_message_text("Contact support : @ton_username")

def main():
    Thread(target=run_flask).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    print("Bot lancé...")
    application.run_polling()

if __name__ == "__main__":
    main()
