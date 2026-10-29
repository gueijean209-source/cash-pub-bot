import os
from flask import Flask
import threading
import telebot
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7528742591:TON_TOKEN_ICI")
MONETAG_LINK = "https://uplcm.com/4/12147475"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# TON HTML DE MINI APP DIRECTEMENT DANS LE CODE - PLUS BESOIN DE templates/
HTML_MINI_APP = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
body{background:#0f1115;color:white;font-family:sans-serif;margin:0;padding:15px;padding-bottom:80px}
.card{background:#1a1f2e;border-radius:20px;padding:20px;margin-bottom:15px}
.solde{font-size:42px;font-weight:bold}
.stats{display:flex;gap:10px;margin-top:15px}
.stat{background:#232a3d;border-radius:15px;padding:15px;flex:1;text-align:center}
.stat b{display:block;font-size:18px}
.stat span{font-size:10px;color:#8a90a5}
.btn-main{background:#4a7bff;width:100%;padding:18px;border:none;border-radius:15px;color:white;font-size:18px;font-weight:bold;margin:15px 0}
.menu{position:fixed;bottom:0;left:0;right:0;background:#1a1f2e;display:flex;justify-content:space-around;padding:15px;border-top:1px solid #232a3d}
</style>
</head>
<body>
<div class="card">
  <div style="color:#8a90a5;font-size:12px">💳 SOLDE</div>
  <div class="solde" id="solde">0 F</div>
  <div class="stats">
    <div class="stat"><b id="total">0 F</b><span>TOTAL GAGNÉ</span></div>
    <div class="stat"><b id="pubs">0</b><span>PUBS REGARDÉES</span></div>
    <div class="stat"><b>0</b><span>TICKETS</span></div>
  </div>
</div>
<button class="btn-main" onclick="regarderPub()">▶ Regarder une pub · Gagner 50 F</button>
<p style="text-align:center;color:#8a90a5;font-size:12px">En quelques secondes — la récompense tombe dans votre solde.</p>
<div class="card">
  <div style="display:flex;justify-content:space-between"><b>✨ TÂCHE SPÉCIALE</b><span style="background:#1e3a2e;color:#4ade80;padding:3px 8px;border-radius:10px;font-size:10px">+25 F</span></div>
  <div style="margin-top:15px">🐥 Regarde 5 pubs</div>
</div>
<div class="menu"><div>🎰<br><small>Roulette</small></div><div style="color:#4a7bff">🏠<br><small>Accueil</small></div><div>🏆<br><small>Classement</small></div></div>
<script>
let solde = parseInt(localStorage.getItem('solde')||'0');
let pubs = parseInt(localStorage.getItem('pubs')||'0');
document.getElementById('solde').innerText = solde+' F';
document.getElementById('pubs').innerText = pubs;
function regarderPub(){
  window.open("https://uplcm.com/4/12147475", "_blank");
  document.querySelector('.btn-main').innerText = "⏳ Attends 15s...";
  setTimeout(()=>{
    solde+=50; pubs+=1;
    localStorage.setItem('solde',solde); localStorage.setItem('pubs',pubs);
    document.getElementById('solde').innerText = solde+' F';
    document.getElementById('pubs').innerText = pubs;
    document.querySelector('.btn-main').innerText = "▶ Regarder une pub · Gagner 50 F";
    alert("✅ +50 F ajouté ! Solde: "+solde+" F");
  },15000);
}
Telegram.WebApp.ready(); Telegram.WebApp.expand();
</script>
</body>
</html>
"""

users = {}
def get_user(uid):
    if uid not in users: users[uid]={"solde":0,"pubs":0}
    return users[uid]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 OUVRIR LA MINI APP", web_app=types.WebAppInfo(url="https://cash-pub-bot.onrender.com/")))
    bot.send_message(message.chat.id, "👋 Bienvenue ! Clique pour ouvrir ta Mini App comme Rewardo 👇", reply_markup=markup)

@app.route('/')
def home():
    return HTML_MINI_APP

@app.route('/verif')
def verif():
    return '<head><meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455"></head>OK'

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
