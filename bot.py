import os
from flask import Flask
import threading
import telebot
from telebot import types

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7528742591:TON_TOKEN_ICI")
MONETAG_LINK = "https://uplcm.com/4/12147475"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

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
#pub-overlay{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:#000000ee;z-index:100;flex-direction:column;align-items:center;justify-content:center;padding:20px;text-align:center}
.timer{font-size:80px;font-weight:bold;color:#4a7bff}
.progress{width:90%;height:10px;background:#232a3d;border-radius:10px;margin-top:20px;overflow:hidden}
.bar{height:100%;background:#4a7bff;width:100%;transition:width 1s linear}
</style>
</head>
<body>

<div id="pub-overlay">
  <div style="font-size:20px;color:#8a90a5">PUBLICITÉ EN COURS...</div>
  <div class="timer" id="count">30</div>
  <div style="margin-top:10px">Ne fermez pas, votre récompense arrive !</div>
  <div class="progress"><div class="bar" id="bar"></div></div>
  <div style="margin-top:20px;color:#8a90a5;font-size:13px">Votre pub : 1xBet - Bonus 200% - Merci de patienter</div>
</div>

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
<p style="text-align:center;color:#8a90a5;font-size:12px">30 secondes = 50 F direct dans ton solde !</p>

<div class="card">
  <b>✨ TÂCHE SPÉCIALE</b> <span style="float:right;background:#1e3a2e;color:#4ade80;padding:3px 8px;border-radius:10px;font-size:10px">+25 F</span><br><br>
  🐥 Regarde 5 pubs
</div>

<script>
let solde = parseInt(localStorage.getItem('solde')||'0');
let pubs = parseInt(localStorage.getItem('pubs')||'0');
document.getElementById('solde').innerText = solde+' F';
document.getElementById('pubs').innerText = pubs;

function regarderPub(){
  window.open("https://uplcm.com/4/12147475", "_blank");
  let overlay = document.getElementById('pub-overlay');
  overlay.style.display='flex';
  let count = 30;
  let timer = setInterval(()=>{
    count--;
    document.getElementById('count').innerText = count;
    document.getElementById('bar').style.width = (count/30*100)+'%';
    if(count<=0){
      clearInterval(timer);
      overlay.style.display='none';
      solde+=50; pubs+=1;
      localStorage.setItem('solde',solde);
      localStorage.setItem('pubs',pubs);
      document.getElementById('solde').innerText = solde+' F';
      document.getElementById('pubs').innerText = pubs;
      document.getElementById('count').innerText = '30';
      document.getElementById('bar').style.width = '100%';
      alert("✅ BRAVO ! +50 F ajouté !\\nSolde: "+solde+" F");
    }
  },1000);
}
Telegram.WebApp.ready(); Telegram.WebApp.expand();
</script>
</body>
</html>
"""

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 OUVRIR LA MINI APP", web_app=types.WebAppInfo(url="https://cash-pub-bot.onrender.com/")))
    bot.send_message(message.chat.id, "👋 Clique pour ouvrir ton app avec timer 30s !", reply_markup=markup)

@app.route('/')
def home(): return HTML_MINI_APP

@app.route('/verif')
def verif(): return '<head><meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455"></head>OK'

def run_bot(): bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
