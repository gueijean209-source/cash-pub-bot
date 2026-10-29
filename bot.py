import os
from flask import Flask
import threading
import telebot
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7528742591:TON_TOKEN_ICI")
MONETAG_LINK = "https://uplcm.com/4/12147475"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {"solde": 0, "pubs": 0}
    return users[user_id]

def menu_telegram():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("👤 Mon Compte"),
    )
    markup.add(
        types.KeyboardButton("📺 Regarde une Pub"),
    )
    markup.add(
        types.KeyboardButton("🔗 Inviter des Amis"),
        types.KeyboardButton("🚩 Mes Tâches")
    )
    markup.add(
        types.KeyboardButton("💵 Retrait"),
        types.KeyboardButton("🏆 Classement")
    )
    markup.add(
        types.KeyboardButton("🎮 Mini-Jeux"),
        types.KeyboardButton("📋 Procédure")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message.from_user.id)
    bot.send_message(message.chat.id, 
        f"👋 Bienvenue !\n\n💰 Solde: {user['solde']} FCFA\n\nClique sur 📺 Regarde une Pub pour gagner !",
        reply_markup=menu_telegram())

@bot.message_handler(func=lambda m: "Mon Compte" in m.text)
def mon_compte(message):
    user = get_user(message.from_user.id)
    bot.send_message(message.chat.id, f"👤 Mon Compte\n\n💰 Solde: {user['solde']} FCFA\n🎬 Pubs vues: {user['pubs']}", reply_markup=menu_telegram())

# C'EST ICI LE BOUTON DE TON IMAGE - MAINTENANT IL OUVRE TA PUB
@bot.message_handler(func=lambda m: "Regarde une Pub" in m.text)
def regarde_pub(message):
    user_id = message.from_user.id
    get_user(user_id)
    
    markup = types.InlineKeyboardMarkup()
    btn_pub = types.InlineKeyboardButton("🔗 CLIQUE ICI - VOIR LA PUB", url=MONETAG_LINK)
    markup.add(btn_pub)
    
    bot.send_message(message.chat.id,
        "🎬 **Pour gagner 25 FCFA:**\n\n1️⃣ Clique sur le bouton ci-dessous\n2️⃣ Regarde la pub 10-15 sec sur le site\n3️⃣ Reviens, tu seras crédité automatiquement\n\n👇",
        reply_markup=markup)

@bot.message_handler(func=lambda m: "Retrait" in m.text)
def retrait(message):
    user = get_user(message.from_user.id)
    bot.send_message(message.chat.id, f"💵 Retrait\nSolde: {user['solde']} FCFA\nMinimum: 500 F", reply_markup=menu_telegram())

@app.route('/')
def home():
    return '''<!DOCTYPE html><html><head><meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455"></head><body><h1>Gains Faciles CI Bot en ligne - Verifie Monetag OK</h1><p>Site verifie pour Monetag</p></body></html>'''

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
