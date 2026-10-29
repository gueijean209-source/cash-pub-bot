import os
from flask import Flask
import threading
import telebot
from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Mémoire simple (solde)
users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {"solde": 0, "pubs": 0}
    return users[user_id]

def menu_principal():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("👤 Mon Compte")
    )
    markup.add(
        types.KeyboardButton("📺 Regarde une Pub")
    )
    markup.add(
        types.KeyboardButton("🔗 Inviter des Amis"),
        types.KeyboardButton("🚩 Mes Tâches")
    )
    markup.add(
        types.KeyboardButton("💵 Retrait"),
        types.KeyboardButton("💰 Bonus")
    )
    markup.add(
        types.KeyboardButton("🎁 Cadeau"),
        types.KeyboardButton("📋 Procédure")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"🎉 **Bienvenue {message.from_user.first_name} !**\n\n💰 Gains Faciles CI - Gagne de l'argent en regardant des pubs !\n\n👇 Choisis une option dans le menu :",
        reply_markup=menu_principal(),
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: m.text == "👤 Mon Compte")
def mon_compte(message):
    user = get_user(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"👤 **MON COMPTE**\n\n🆔 ID: {message.from_user.id}\n👤 Nom: {message.from_user.first_name}\n\n💰 Solde: {user['solde']} FCFA\n📺 Pubs vues: {user['pubs']}\n\n🔗 Lien parrainage:\nhttps://t.me/cash_pub_ci_bot?start={message.from_user.id}",
        reply_markup=menu_principal()
    )

@bot.message_handler(func=lambda m: m.text == "📺 Regarde une Pub")
def regarder_pub(message):
    user = get_user(message.from_user.id)
    user['solde'] += 50
    user['pubs'] += 1
    bot.send_message(
        message.chat.id,
        f"✅ Pub vue ! +50 FCFA\n\n💰 Nouveau solde: {user['solde']} FCFA\n\n⏳ Reviens dans 10 sec pour une autre pub !",
        reply_markup=menu_principal()
    )

@bot.message_handler(func=lambda m: m.text == "🔗 Inviter des Amis")
def inviter(message):
    bot.send_message(
        message.chat.id,
        f"🔗 **INVITER DES AMIS**\n\nGagne 10% sur chaque ami !\n\nTon lien:\n`https://t.me/cash_pub_ci_bot?start={message.from_user.id}`\n\nPartage-le sur WhatsApp / Facebook !",
        parse_mode="Markdown",
        reply_markup=menu_principal()
    )

@bot.message_handler(func=lambda m: m.text == "🚩 Mes Tâches")
def taches(message):
    user = get_user(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"🚩 **MES TÂCHES**\n\n✅ Tâche 1: Regarder 5 pubs ({user['pubs']}/5)\n✅ Tâche 2: Inviter 3 amis (0/3)\n\nRécompense: 500 FCFA par tâche !",
        reply_markup=menu_principal()
    )

@bot.message_handler(func=lambda m: m.text == "💵 Retrait")
def retrait(message):
    user = get_user(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"💵 **RETRAIT**\n\n💰 Solde: {user['solde']} FCFA\n\nMinimum retrait: 3000 FCFA\n\nMéthodes: Wave, MTN, Orange\n\nTape: /retrait 3000 0700000000",
        reply_markup=menu_principal()
    )

@bot.message_handler(func=lambda m: m.text in ["💰 Bonus", "🎁 Cadeau", "📋 Procédure"])
def autres(message):
    bot.send_message(
        message.chat.id,
        f"🚀 Fonction **{message.text}** bientôt disponible !\n\nContinue à regarder les pubs pour gagner !",
        reply_markup=menu_principal()
    )

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

@app.route('/')
def home():
    return "Gains Faciles CI Bot en ligne !"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
