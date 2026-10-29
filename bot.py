import os
import threading
from flask import Flask, request, jsonify
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, WebAppInfo

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://cash-pub-bot.onrender.com").rstrip("/")

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

users = {}

def get_user(uid, name=""):
    if uid not in users:
        users[uid] = {"nom": name or "Utilisateur", "solde": 0, "tickets": 0, "amis": 0, "pubs": 0}
    return users[uid]

def menu_principal():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("👤 Mon Compte", "📺 Regarde une Pub")
    markup.add("🔗 Inviter des Amis", "🚩 Mes Tâches")
    markup.add("💵 Retrait", "🏆 Classement")
    markup.add("🎮 Mini-Jeux", "📋 Procédure")
    return markup

# PAGE WATCH AVEC CHRONO 30s
WATCH_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455">
<title>Pub 30s</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="https://quge5.com/88/tag.min.js" data-zone="303312" async data-cfasync="false"></script>
<style>
body{background:#0a0e15;color:#fff;font-family:Arial;margin:0;padding:0;text-align:center}
.top{position:fixed;top:0;left:0;right:0;background:#111827;padding:10px;display:flex;justify-content:space-between;align-items:center;z-index:100;border-bottom:1px solid #222}
.timer{font-size:18px;font-weight:900;background:#1f2937;padding:6px 14px;border-radius:20px}
.bar-bg{position:fixed;top:46px;left:0;right:0;height:4px;background:#1f2937}
.bar{height:100%;background:linear-gradient(90deg,#4a7bff,#6a5cff);width:100%;transition:width 1s linear}
.content{padding:70px 16px 20px}
.ad-box{background:#1a1f2e;border-radius:16px;padding:20px;margin:14px 0;border:1px solid #232a3d}
.btn{width:100%;padding:16px;border:none;border-radius:14px;font-weight:900;font-size:16px;margin-top:12px}
.btn-wait{background:#232a3d;color:#8a90a5}
.btn-ok{background:linear-gradient(135deg,#4a7bff,#6a5cff);color:white;display:none}
</style>
</head><body>
<div class="top"><button onclick="Telegram.WebApp.close()" style="background:#232a3d;color:#fff;border:none;padding:6px 12px;border-radius:8px">✕ Fermer</button><div class="timer" id="timer">00:30</div><div style="width:60px"></div></div>
<div class="bar-bg"><div class="bar" id="bar"></div></div>
<div class="content">
  <h2 style="margin-top:10px">📺 Pub en cours...</h2>
  <p style="color:#8a90a5">Reste 30 secondes, ne ferme pas !<br>Tu gagnes +50 FCFA automatiquement</p>
  <div class="ad-box">
    <p style="font-size:13px;color:#4ade80">✅ Monetag Zone 303312 + Direct Links actifs</p>
    <div style="background:#0f1115;padding:30px;border-radius:12px;margin:10px 0">PUBLICITÉ<br><small>(Monetag affiche ici)</small></div>
    <button class="btn btn-wait" id="waitBtn">⏳ Attends 30s...</button>
    <button class="btn btn-ok" id="okBtn" onclick="claim()">✅ Réclamer 50 FCFA</button>
  </div>
  <p style="font-size:11px;color:#666">Après 30s ça crédite auto et ça ferme</p>
</div>
<script>
let uid = new URLSearchParams(window.location.search).get('uid') || '0';
let timeLeft = 30;
let timerEl = document.getElementById('timer');
let barEl = document.getElementById('bar');
let waitBtn = document.getElementById('waitBtn');
let okBtn = document.getElementById('okBtn');

if(window.Telegram && Telegram.WebApp){ Telegram.WebApp.ready(); Telegram.WebApp.expand(); }

let interval = setInterval(()=>{
  timeLeft--;
  let m = '00:' + (timeLeft<10?'0':'') + timeLeft;
  timerEl.innerText = m;
  barEl.style.width = (timeLeft/30*100)+'%';
  waitBtn.innerText = '⏳ Attends '+timeLeft+'s...';
  // Ouvre un direct link à 15s pour plus de revenu
  if(timeLeft==15){ try{ window.open("https://uplcm.com/4/12147480","_blank"); }catch(e){} }
  if(timeLeft<=0){
    clearInterval(interval);
    timerEl.innerText='00:00';
    waitBtn.style.display='none';
    okBtn.style.display='block';
    // Auto crédit après 1s
    setTimeout(claim, 800);
  }
},1000);

function claim(){
  fetch('/api/credit?uid='+uid)
    .then(r=>r.json())
    .then(d=>{
      okBtn.innerText='✅ +50 FCFA crédité ! Solde: '+d.solde+' F';
      okBtn.style.background='#16a34a';
      setTimeout(()=>{ if(window.Telegram && Telegram.WebApp){ Telegram.WebApp.close(); } else { window.close(); } }, 1500);
    });
}
</script></body></html>
"""

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    name = message.from_user.first_name
    args = message.text.split()
    if len(args) > 1:
        try:
            parrain_id = int(args[1])
            if parrain_id != uid and parrain_id in users:
                users[parrain_id]["amis"] += 1
                users[parrain_id]["solde"] += 500
                bot.send_message(parrain_id, f"🎉 +1 filleul ! +500 FCFA. Total amis: {users[parrain_id]['amis']}")
        except: pass
    u = get_user(uid, name)
    bot.send_message(message.chat.id, f"👋 Ravi de te revoir, {u['nom']} !\n\nPrêt à booster tes gains aujourd'hui ?\nAccomplis des tâches, regarde des pubs,\njoue aux mini-jeux ou invite des amis.\n\n👇 Choisis une option dans le menu ci-dessous :", reply_markup=menu_principal())

@bot.message_handler(func=lambda m: m.text and "Mon Compte" in m.text)
def mon_compte(message):
    u = get_user(message.from_user.id, message.from_user.first_name)
    bot.send_message(message.chat.id, f"👤 Nom : {u['nom']}\n\n💰 Solde : {u['solde']:,} FCFA\n🎟️ Tickets disponibles : {u['tickets']}\n👥 Amis invités : {u['amis']}\n📺 Pubs regardées : {u['pubs']}\n\n📌 Retrait possible dès 20000 FCFA.\n💡 Invite des amis pour avancer plus vite.", reply_markup=menu_principal())

@bot.message_handler(func=lambda m: m.text and "Regarde une Pub" in m.text)
def regarde_pub(message):
    uid = message.from_user.id
    get_user(uid)
    markup = InlineKeyboardMarkup()
    watch_url = f"{WEBAPP_URL}/watch?uid={uid}"
    markup.add(InlineKeyboardButton("📺 Regarder (30s chrono)", web_app=WebAppInfo(url=watch_url)))
    bot.send_message(message.chat.id, "📺 Regarde une pub et gagne 50 FCFA à chaque fois.\n\n⏱️ Chrono 30 secondes obligatoire. Reste jusqu'au bout, ça crédite automatiquement !", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text and "Retrait" in m.text)
def retrait(message):
    u = get_user(message.from_user.id)
    if u['solde'] >= 20000: bot.send_message(message.chat.id, f"✅ Tu peux retirer {u['solde']} FCFA ! Envoie ton numéro Wave.")
    else: bot.send_message(message.chat.id, "🚫 Le retrait est possible à partir de\n20,000 FCFA.\n\nInvite des amis ou complète des tâches\npour atteindre ce montant 💸", reply_markup=menu_principal())

@bot.message_handler(func=lambda m: m.text and "Inviter" in m.text)
def inviter(message):
    bot.send_message(message.chat.id, f"🔗 Ton lien :\nhttps://t.me/{bot.get_me().username}?start={message.from_user.id}\n\n500 FCFA / ami !", reply_markup=menu_principal())

@bot.message_handler(func=lambda m: True)
def all_other(message): bot.send_message(message.chat.id, "👇 Choisis une option dans le menu ci-dessous :", reply_markup=menu_principal())

@app.route('/')
def index(): return "<h1>Bot en ligne - Monetag OK</h1>"
@app.route('/watch')
def watch(): return WATCH_HTML
@app.route('/api/credit')
def credit():
    uid = request.args.get('uid', type=int)
    if not uid or uid not in users: return jsonify({"error": "user not found", "solde": 0})
    users[uid]["solde"] += 50
    users[uid]["pubs"] += 1
    return jsonify({"ok": True, "solde": users[uid]["solde"]})
@app.route('/verif')
def verif(): return '<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455"> Verif OK'

def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()
