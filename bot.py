import os
import threading
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, WebAppInfo

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = "https://cash-pub-bot.onrender.com"
GROUP_LINK = "https://t.me/+TH2UW0jyWthlM2U0"

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# Stockage simple en mémoire
users = {}

HTML_PAGE = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cash Pub</title>
<script src="https://quge5.com/88/tag.min.js" data-zone="303312" async data-cfasync="false"></script>
</head><body style="background:#0f1115;color:white;text-align:center;padding:50px;font-family:Arial">
<h1>💰 Cash Pub Bot est en ligne</h1>
<p>Monetag Zone 303312 active</p>
<p>Direct Links actifs</p>
</body></html>
"""

def get_user(uid, name="Jean"):
    if uid not in users:
        users[uid] = {"nom": name, "solde": 1050, "tickets": 0, "amis": 5, "pubs": 264}
    return users[uid]

def menu_principal():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("👤 Mon Compte", "📺 Regarde une Pub")
    markup.add("🔗 Inviter des Amis", "🚩 Mes Tâches")
    markup.add("💵 Retrait", "🏆 Classement")
    markup.add("🎮 Mini-Jeux", "📋 Procédure")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    u = get_user(message.from_user.id, message.from_user.first_name)
    bot.send_message(message.chat.id,
        f"👋 Ravi de te revoir, {u['nom']} !\n\n"
        "Prêt à booster tes gains aujourd'hui ?\n"
        "Accomplis des tâches, regarde des pubs,\n"
        "joue aux mini-jeux ou invite des amis.\n\n"
        "👇 Choisis une option dans le menu ci-dessous :",
        reply_markup=menu_principal())

@bot.message_handler(func=lambda m: m.text and "Mon Compte" in m.text)
def mon_compte(message):
    u = get_user(message.from_user.id, message.from_user.first_name)
    bot.send_message(message.chat.id,
        f"👤 Nom : {u['nom']}\n\n"
        f"💰 Solde : {u['solde']:,} FCFA\n"
        f"🎟️ Tickets disponibles : {u['tickets']}\n"
        f"👥 Amis invités : {u['amis']}\n"
        f"📺 Pubs regardées : {u['pubs']}\n\n"
        f"📌 Retrait possible dès 20000 FCFA.\n"
        f"💡 Invite des amis pour avancer plus vite.",
        reply_markup=menu_principal())

@bot.message_handler(func=lambda m: m.text and "Regarde une Pub" in m.text)
def regarde_pub_text(message):
    markup = InlineKeyboardMarkup()
    # Bouton qui ouvre ton Direct Link + Monetag
    markup.add(InlineKeyboardButton("📺 Regarde", url="https://uplcm.com/4/12147475"))
    markup.add(InlineKeyboardButton("🚀 Ouvrir Mini App", web_app=WebAppInfo(url=WEBAPP_URL)))
    bot.send_message(message.chat.id,
        "📺 Regarde une pub et gagne 50 FCFA à chaque fois.",
        reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and "Retrait" in m.text)
def retrait(message):
    u = get_user(message.from_user.id)
    if u['solde'] >= 20000:
        bot.send_message(message.chat.id, f"✅ Tu peux retirer {u['solde']} FCFA ! Envoie ton numéro Wave.")
    else:
        bot.send_message(message.chat.id,
            "🚫 Le retrait est possible à partir de\n"
            "20,000 FCFA.\n\n"
            "Invite des amis ou complète des tâches\n"
            "pour atteindre ce montant 💸",
            reply_markup=menu_principal())

@bot.message_handler(func=lambda m: m.text and "Inviter" in m.text)
def inviter(message):
    bot.send_message(message.chat.id,
        "🔗 Ton lien d'invitation :\n"
        f"https://t.me/{bot.get_me().username}?start={message.from_user.id}\n\n"
        "500 FCFA par ami invité !",
        reply_markup=menu_principal())

@bot.message_handler(func=lambda m: True)
def all_other(message):
    bot.send_message(message.chat.id,
        "👇 Choisis une option dans le menu ci-dessous :",
        reply_markup=menu_principal())

@app.route('/')
def index():
    return HTML_PAGE

@app.route('/verif')
def verif():
    return '<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455"> Verif OK'

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()
