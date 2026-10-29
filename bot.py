import os
from flask import Flask
import threading
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7528742591:TON_TOKEN_ICI")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {"solde": 0}
    return users[user_id]

def menu_principal():
    from telebot import types
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Solde", "🎬 Voir pub", "💸 Retrait")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message.from_user.id)
    bot.send_message(message.chat.id, f"Bienvenue ! Solde: {user['solde']} F", reply_markup=menu_principal())

@bot.message_handler(func=lambda m: m.text == "💰 Solde")
def solde(message):
    user = get_user(message.from_user.id)
    bot.send_message(message.chat.id, f"💰 Solde: {user['solde']} F", reply_markup=menu_principal())

@app.route('/')
def home():
    return '''<!DOCTYPE html><html><head><meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455"></head><body><h1>Gains Faciles CI Bot en ligne - Verifie Monetag OK</h1><p>Site verifie pour Monetag</p></body></html>'''

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
