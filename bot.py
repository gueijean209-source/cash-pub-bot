import os, threading, time, logging, json, requests
from flask import Flask, request, jsonify
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, WebAppInfo

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://cash-pub-bot.onrender.com").rstrip("/")
NPOINT_ID = os.environ.get("NPOINT_ID", "") # Si tu l'as créé sur npoint.io, sinon laisse vide

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

NPOINT_URL = f"https://api.npoint.io/{NPOINT_ID}" if NPOINT_ID else None

def load_users():
    if NPOINT_URL:
        try:
            r = requests.get(NPOINT_URL, timeout=5)
            if r.status_code==200 and r.text.strip() not in ["{}", ""]:
                return r.json()
        except: pass
    if os.path.exists("users.json"):
        try:
            with open("users.json",'r') as f: return json.load(f)
        except: pass
    return {}

def save_users():
    try:
        with open("users.json",'w') as f: json.dump(users,f)
        if NPOINT_URL:
            threading.Thread(target=lambda: requests.post(NPOINT_URL, json=users, timeout=5), daemon=True).start()
    except Exception as e: logging.error(f"Save error {e}")

users = load_users()
logging.info(f"Loaded {len(users)} users")

def get_user(uid, name=""):
    uid_str=str(uid)
    if uid_str not in users:
        users[uid_str]={"nom":name or "Utilisateur","solde":0,"tickets":0,"amis":0,"pubs":0}
        save_users()
    return users[uid_str]

def menu_principal():
    m=ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    m.add("👤 Mon Compte","📺 Regarde une Pub")
    m.add("🔗 Inviter des Amis","🚩 Mes Tâches")
    m.add("💵 Retrait","🏆 Classement")
    m.add("🎮 Mini-Jeux","📋 Procédure")
    return m

# ICI TON NOUVEAU CODE MULTITAG 303393
WATCH_HTML = """
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455">
<title>Pub 30s - Gagne 50F</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>

<!-- ANCIEN TAG 303312 -->
<script src="https://quge5.com/88/tag.min.js" data-zone="303312" async data-cfasync="false"></script>

<!-- NOUVEAU MULTITAG ALL-IN-ONE 303393 - TON CODE QUE TU VIENS D'AVOIR -->
<script src="https://quge5.com/88/tag.min.js" data-zone="303393" async data-cfasync="false"></script>

<style>body{background:#0a0e15;color:#fff;font-family:Arial;margin:0;text-align:center} .top{position:fixed;top:0;left:0;right:0;background:#111827;padding:10px;display:flex;justify-content:space-between;z-index:100} .timer{font-size:18px;font-weight:900;background:#1f2937;padding:6px 14px;border-radius:20px} .bar-bg{position:fixed;top:46px;left:0;right:0;height:4px;background:#1f2937} .bar{height:100%;background:#4a7bff;width:100%;transition:width 1s linear} .content{padding:70px 16px 20px} .ad-box{background:#1a1f2e;border-radius:16px;padding:20px;margin:14px 0;border:1px solid #232a3d} .btn{width:100%;padding:16px;border:none;border-radius:14px;font-weight:900;font-size:16px;margin-top:12px} .btn-wait{background:#232a3d;color:#8a90a5} .btn-ok{background:#16a34a;color:white;display:none}</style>
</head><body>
<div class="top"><button onclick="Telegram.WebApp.close()" style="background:#232a3d;color:#fff;border:none;padding:6px 12px;border-radius:8px">✕ Fermer</button><div class="timer" id="timer">00:30</div><div style="width:60px"></div></div>
<div class="bar-bg"><div class="bar" id="bar"></div></div>
<div class="content"><h2>📺 Pub en cours... +50 FCFA</h2><p style="color:#8a90a5">Reste 30s, ne ferme pas ! 2 pubs chargées</p><div class="ad-box"><div style="background:#0f1115;padding:30px;border-radius:12px">MULTITAG ACTIF - Gains x3</div><button class="btn btn-wait" id="waitBtn">⏳ Attends 30s...</button><button class="btn btn-ok" id="okBtn" onclick="claim()">✅ Réclamer 50 FCFA</button></div></div>
<script>
let uid=new URLSearchParams(window.location.search).get('uid')||'0';let timeLeft=30;let timerEl=document.getElementById('timer');let barEl=document.getElementById('bar');let waitBtn=document.getElementById('waitBtn');let okBtn=document.getElementById('okBtn');if(window.Telegram&&Telegram.WebApp){Telegram.WebApp.ready();Telegram.WebApp.expand();}let interval=setInterval(()=>{timeLeft--;timerEl.innerText='00:'+(timeLeft<10?'0':'')+timeLeft;barEl.style.width=(timeLeft/30*100)+'%';waitBtn.innerText='⏳ Attends '+timeLeft+'s...';if(timeLeft<=0){clearInterval(interval);waitBtn.style.display='none';okBtn.style.display='block';setTimeout(claim,800);}},1000);function claim(){fetch('/api/credit?uid='+uid).then(r=>r.json()).then(d=>{okBtn.innerText='✅ +50 FCFA ! Solde: '+d.solde+' F';setTimeout(()=>{if(window.Telegram&&Telegram.WebApp){Telegram.WebApp.close();}},1200);});}
</script></body></html>
"""

@bot.message_handler(commands=['start'])
def start(message):
    try:
        uid=message.from_user.id; name=message.from_user.first_name; args=message.text.split()
        if len(args)>1:
            try:
                parrain_id=str(args[1]); uid_str=str(uid)
                if parrain_id!=uid_str and parrain_id in users:
                    users[parrain_id]["amis"]+=1; users[parrain_id]["solde"]+=500; save_users()
                    bot.send_message(int(parrain_id), f"🎉 +1 filleul ! +500 FCFA. Total: {users[parrain_id]['amis']}")
            except: pass
        u=get_user(uid,name); save_users()
        bot.send_message(message.chat.id, f"👋 Ravi de te revoir, {u['nom']} !\n\nPrêt à booster tes gains ?\n\n👇 Choisis une option :", reply_markup=menu_principal())
    except Exception as e: logging.error(e)

@bot.message_handler(func=lambda m: True)
def all_handler(message):
    try:
        txt=message.text or ""; uid=message.from_user.id; u=get_user(uid, message.from_user.first_name)
        if "Mon Compte" in txt:
            bot.send_message(message.chat.id, f"👤 Nom : {u['nom']}\n\n💰 Solde : {u['solde']:,} FCFA\n🎟️ Tickets : {u['tickets']}\n👥 Amis : {u['amis']}\n📺 Pubs : {u['pubs']}\n\n📌 Retrait dès 20000 FCFA.\nMultitag Actif ✅", reply_markup=menu_principal())
        elif "Regarde une Pub" in txt:
            mk=InlineKeyboardMarkup(); mk.add(InlineKeyboardButton("📺 Regarder (30s) - Multitag x3", web_app=WebAppInfo(url=f"{WEBAPP_URL}/watch?uid={uid}")))
            bot.send_message(message.chat.id, "📺 Regarde une pub et gagne 50 FCFA.\n\n💰 Nouveau : Multitag activé, tu rapportes 3x plus !", reply_markup=mk)
        elif "Retrait" in txt:
            bot.send_message(message.chat.id, f"✅ Tu peux retirer {u['solde']} F" if u['solde']>=20000 else "🚫 Retrait à partir de 20,000 FCFA.", reply_markup=menu_principal())
        elif "Inviter" in txt:
            bot.send_message(message.chat.id, f"🔗 Ton lien :\nhttps://t.me/{bot.get_me().username}?start={uid}\n\n500 FCFA / ami !", reply_markup=menu_principal())
        else: bot.send_message(message.chat.id, "👇 Choisis une option :", reply_markup=menu_principal())
    except Exception as e: logging.error(e)

@app.route('/')
def index(): return f"<h1>Bot V15 MULTITAG 303393 - {len(users)} users - Gains x3</h1>"
@app.route('/watch')
def watch(): return WATCH_HTML
@app.route('/api/credit')
def credit():
    uid=str(request.args.get('uid')); 
    if uid not in users: return jsonify({"solde":0})
    users[uid]["solde"]+=50; users[uid]["pubs"]+=1; save_users()
    return jsonify({"ok":True,"solde":users[uid]["solde"]})
@app.route('/verif')
def verif(): return '<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455"> Verif OK'

def run_flask(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
def run_bot():
    while True:
        try: bot.infinity_polling(timeout=60, long_polling_timeout=60, skip_pending=True)
        except Exception as e: logging.error(f"Polling crash {e}"); time.sleep(5)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
