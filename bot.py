import os
import threading
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, WebAppInfo

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = "https://cash-pub-bot.onrender.com"

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

users = {}  # {user_id: {nom, solde, tickets, amis, pubs}}

HTML_PAGE = """
<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Cash Pub</title>
<script src="https://quge5.com/88/tag.min.js" data-zone="303312" async data-cfasync="false"></script>
</head><body style="background:#0f1115;color:white;text-align:center;padding:50px;font-family:Arial">
<h1>💰 Cash Pub Bot en ligne - V9</h1></body></html>
"""

def get_user(uid, name=""):
    if uid not in users:
        # NOUVEAU UTILISATEUR = 0 partout, pas 1050
        users[uid] = {"nom": name or "Utilisateur", "solde": 0, "tickets": 0, "amis": 0, "pubs": 0}
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
    uid = message.from_user.id
    name = message.from_user.first_name
    args = message.text.split()
    
    # Gestion parrainage: /start 123456
    if len(args) > 1:
        try:
            parrain_id = int(args[1])
            if parrain_id != uid and parrain_id in users:
                users[parrain_id]["amis"] += 1
                users[parrain_id]["solde"] += 500
                bot.send_message(parrain_id, f"🎉 +1 filleul ! +500 FCFA. Tu as maintenant {users[parrain_id]['amis']} amis.")
        except:
            pass

    u = get_user(uid, name)
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
    u = get_user(message.from_user.id)
    # On ajoute 50 FCFA à chaque fois qu'il clique
    u["solde"] += 50
    u["pubs"] += 1
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📺 Regarde encore +50F", url="https://uplcm.com/4/12147475"))
    markup.add(InlineKeyboardButton("🚀 Ouvrir Mini App", web_app=WebAppInfo(url=WEBAPP_URL)))
    
    bot.send_message(message.chat.id,
        f"📺 Regarde une pub et gagne 50 FCFA à chaque fois.\n\n"
        f"✅ +50 FCFA ajouté ! Nouveau solde : {u['solde']} FCFA",
        reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and "Retrait" in m.text)
def retrait(message):
    u = get_user(message.from_user.id)
    if u['solde'] >= 20000:
        bot.send_message(message.chat.id, f"✅ Bravo {u['nom']} ! Tu peux retirer {u['solde']} FCFA.\nEnvoie ton numéro Wave / MTN.")
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
        f"🔗 Ton lien d'invitation :\n"
        f"https://t.me/{bot.get_me().username}?start={message.from_user.id}\n\n"
        "500 FCFA par ami invité !",
        reply_markup=menu_principal())

@bot.message_handler(func=lambda m: True)
def all_other(message):
    bot.send_message(message.chat.id, "👇 Choisis une option dans le menu ci-dessous :", reply_markup=menu_principal())

@app.route('/')
def index(): return HTML_PAGE
@app.route('/verif')
def verif(): return '<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455"> Verif OK'
def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()
