import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "TON_TOKEN_ICI")
WEBAPP_URL = "https://cash-pub-bot.onrender.com"
GROUP_LINK = "https://t.me/+TH2UW0jyWthlM2U0"

app = Flask(__name__)

HTML_MINI_APP = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455">
<title>Cash Pub V6</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="https://quge5.com/88/tag.min.js" data-zone="303312" async data-cfasync="false"></script>
<style>
*{{box-sizing:border-box}} body{{background:#0f1115;color:white;font-family:sans-serif;margin:0;padding:12px;padding-bottom:30px}}
.card{{background:#1a1f2e;border-radius:20px;padding:18px;margin-bottom:12px;border:1px solid #232a3d}}
.solde{{font-size:48px;font-weight:900;color:#4a7bff}} .solde-label{{color:#8a90a5;font-size:11px;letter-spacing:1px}}
.stats{{display:flex;gap:7px;margin-top:12px}} .stat{{background:#232a3d;border-radius:12px;padding:10px;flex:1;text-align:center}} .stat b{{display:block;font-size:14px}} .stat span{{font-size:8px;color:#8a90a5}}
.btn-main{{background:linear-gradient(135deg,#4a7bff,#6a5cff);width:100%;padding:18px;border:none;border-radius:16px;color:white;font-size:18px;font-weight:900;margin:8px 0;box-shadow:0 10px 20px rgba(74,123,255,0.3)}}
.btn-task{{background:#1a2a1f;border:1px solid #2d6a4f;width:100%;padding:14px;border-radius:14px;color:#4ade80;font-size:14px;font-weight:bold;margin:6px 0;display:flex;justify-content:space-between;align-items:center}}
.btn-task.done{{background:#232a3d;color:#8a90a5;border-color:#232a3d}} .btn-sec{{background:#232a3d;width:100%;padding:14px;border:none;border-radius:14px;color:#8a90a5;font-size:14px;margin:6px 0}}
#pub-overlay{{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.95);z-index:999;flex-direction:column;align-items:center;justify-content:center;padding:20px;text-align:center}}
.timer{{font-size:90px;font-weight:900;color:#4a7bff}} .progress{{width:90%;height:10px;background:#232a3d;border-radius:10px;margin-top:15px;overflow:hidden}} .bar{{height:100%;background:#4a7bff;width:100%;transition:width 1s linear}}
.lock{{background:#2a1f1f;border:1px solid #6a2a2a;border-radius:14px;padding:12px;margin:10px 0;font-size:12px;line-height:1.6}}
</style>
</head>
<body>
<div id="pub-overlay">
  <div style="background:#4a7bff;color:white;padding:6px 12px;border-radius:20px;font-size:12px">PUBLICITÉ EN COURS</div>
  <div class="timer" id="count">30</div>
  <div style="margin-top:5px">+50 F dans <span id="c2">30</span>s</div>
  <div class="progress"><div class="bar" id="bar"></div></div>
  <div style="font-size:11px;color:#8a90a5;margin-top:10px">2 pubs tournent - Double revenu Monetag</div>
</div>

<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 4px">
  <b>💰 CASH PUB V6</b>
  <span style="background:#232a3d;padding:5px 10px;border-radius:20px;font-size:11px">👥 <span id="par">0</span>/5 filleuls</span>
</div>

<div class="card">
  <div class="solde-label">💳 SOLDE DISPONIBLE</div>
  <div class="solde" id="solde">0 F</div>
  <div class="stats">
    <div class="stat"><b id="total">0 F</b><span>TOTAL</span></div>
    <div class="stat"><b id="pubs">0</b><span>PUBS</span></div>
    <div class="stat"><b id="par2">0</b><span>FILLEULS</span></div>
  </div>
  <div id="lockInfo"></div>
</div>

<button class="btn-main" onclick="regarderPub()">▶ REGARDER UNE PUB • +50 F</button>

<div class="card">
  <div style="font-weight:bold;margin-bottom:10px">📋 TÂCHES OBLIGATOIRES (pour retirer)</div>
  <button class="btn-task" id="taskGroup" onclick="doTaskGroup()">
    <span>📢 Rejoindre le groupe privé</span><span id="tgText">+100 F >></span>
  </button>
  <button class="btn-task" id="taskInvite" onclick="invite()">
    <span>👥 Inviter 5 amis (500F / ami)</span><span id="invText">0/5</span>
  </button>
  <div style="font-size:10px;color:#8a90a5;margin-top:8px">Conditions retrait: Groupe + 5 filleuls + 30.000F</div>
</div>

<button class="btn-sec" onclick="invite()">🔗 Lien de parrainage • 500F / ami</button>
<button class="btn-sec" onclick="retirer()">💵 Retrait • MIN 30.000F</button>

<div style="text-align:center;color:#5a627a;font-size:10px;margin-top:15px">
  Monetag MultiTag Zone 303312 actif<br>Direct Link 12147475 + 12147480
</div>

<script>
let solde=parseInt(localStorage.getItem('solde')||'0');
let pubs=parseInt(localStorage.getItem('pubs')||'0');
let total=parseInt(localStorage.getItem('total')||'0');
let parrainages=parseInt(localStorage.getItem('parrainages')||'0');
let taskGroupDone=localStorage.getItem('taskGroupDone')==='true';
const DIRECT_LINKS=["https://uplcm.com/4/12147475","https://uplcm.com/4/12147480"];
const GROUP_LINK="{GROUP_LINK}";

function refreshUI(){{
  document.getElementById('solde').innerText=solde+' F';
  document.getElementById('pubs').innerText=pubs;
  document.getElementById('total').innerText=total+' F';
  document.getElementById('par').innerText=parrainages;
  document.getElementById('par2').innerText=parrainages;
  document.getElementById('invText').innerText=parrainages+'/5';
  let lockDiv=document.getElementById('lockInfo');
  if(parrainages<5||solde<30000||!taskGroupDone){{
    lockDiv.innerHTML=`<div class="lock">🔒 Retrait bloqué:<br>${{taskGroupDone?'✅':'❌'}} Groupe Telegram<br>${{parrainages>=5?'✅':'❌'}} Parrainages: ${{parrainages}}/5<br>${{solde>=30000?'✅':'❌'}} Solde: ${{solde}}/30000 F</div>`;
  }}else{{
    lockDiv.innerHTML=`<div style="background:#1e3a2e;border-radius:12px;padding:10px;margin-top:10px;color:#4ade80;font-size:12px;text-align:center">✅ Tu peux retirer !</div>`;
  }}
  if(taskGroupDone){{document.getElementById('taskGroup').classList.add('done');document.getElementById('tgText').innerText='✅ Fait';}}
}}
refreshUI();

function doTaskGroup(){{
  if(taskGroupDone){{alert("Déjà fait ✅");return;}}
  window.open(GROUP_LINK,"_blank");
  setTimeout(()=>{{
    if(confirm("As-tu bien rejoint le groupe Telegram ?\\nClique OK pour recevoir 100F")){{
      taskGroupDone=true;solde+=100;total+=100;
      localStorage.setItem('taskGroupDone','true');
      localStorage.setItem('solde',solde);
      localStorage.setItem('total',total);
      refreshUI();
      alert("✅ +100 F ajouté ! Merci d'avoir rejoint le groupe !");
    }}
  }},3000);
}}

function regarderPub(){{
  window.open(DIRECT_LINKS[pubs%2],"_blank");
  let overlay=document.getElementById('pub-overlay');
  overlay.style.display='flex';
  let count=30;
  let timer=setInterval(()=>{{
    count--;
    document.getElementById('count').innerText=count;
    document.getElementById('c2').innerText=count;
    document.getElementById('bar').style.width=(count/30*100)+'%';
    if(count==15){{window.open(DIRECT_LINKS[1],"_blank");}}
    if(count<=0){{
      clearInterval(timer);
      overlay.style.display='none';
      solde+=50;pubs+=1;total+=50;
      if(pubs%10==0){{solde+=100;}}
      localStorage.setItem('solde',solde);
      localStorage.setItem('pubs',pubs);
      localStorage.setItem('total',total);
      refreshUI();
      document.getElementById('count').innerText='30';
      document.getElementById('bar').style.width='100%';
      if(window.Telegram&&Telegram.WebApp.HapticFeedback){{Telegram.WebApp.HapticFeedback.notificationOccurred('success');}}
    }}
  }},1000);
}}

function invite(){{
  let refCode=localStorage.getItem('myRef')||Math.floor(Math.random()*90000+10000);
  localStorage.setItem('myRef',refCode);
  let link="https://t.me/GainsFacilesCI_bot?start=ref_"+refCode;
  prompt("Copie ton lien de parrainage (500F par ami):",link);
  if(confirm("TEST: Ajouter 1 filleul pour voir que ça marche ?\\n(En vrai, ça s'ajoute auto quand ton ami clique)")){{
    parrainages+=1;solde+=500;total+=500;
    localStorage.setItem('parrainages',parrainages);
    localStorage.setItem('solde',solde);
    localStorage.setItem('total',total);
    refreshUI();
    alert("🎉 Nouveau filleul ! +500 F");
  }}
}}

function retirer(){{
  if(!taskGroupDone){{alert("❌ Tu dois d'abord rejoindre le groupe Telegram !\\nVa dans TÂCHES > Rejoindre");return;}}
  if(parrainages<5){{alert("❌ Il te faut 5 filleuls minimum !\\nTu as: "+parrainages+"/5\\n\\nPartage ton lien !");return;}}
  if(solde<30000){{alert("❌ Solde insuffisant !\\nTu as: "+solde+" F / 30000 F\\nIl te manque: "+(30000-solde)+" F");return;}}
  let num=prompt("✅ Bravo ! Conditions remplies:\\n✅ Groupe rejoint\\n✅ "+parrainages+"/5 filleuls\\n✅ "+solde+" F\\n\\nEntre ton numéro Wave / Orange Money:");
  if(num){{alert("✅ DEMANDE ENVOYÉE !\\nNuméro: "+num+"\\nMontant: "+solde+" F\\nTu seras payé dans 24h sur Wave.");solde=0;localStorage.setItem('solde',0);refreshUI();}}
}}
Telegram.WebApp.ready();Telegram.WebApp.expand();
</script>
</body>
</html>
"""

# CLAVIER EXACT COMME TA CAPTURE
MENU_KEYBOARD = ReplyKeyboardMarkup(
    [
        ["👤 Mon Compte", "📺 Regarde une Pub"],
        ["🔗 Inviter des Amis", "🚩 Mes Tâches"],
        ["💵 Retrait", "🏆 Classement"],
        ["🎮 Mini-Jeux", "📋 Procédure"]
    ],
    resize_keyboard=True
)

def get_inline_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 OUVRIR LA MINI APP", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("📢 Rejoindre le groupe", url=GROUP_LINK)]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenue sur Gains Faciles CI !\n\n"
        "💰 50F par pub (30s)\n"
        "👥 500F par filleul (5 min)\n"
        "📢 100F pour rejoindre le groupe\n"
        "💸 Retrait min 30.000F\n\n"
        "👇 Clique pour ouvrir ton app avec timer 30s !",
        reply_markup=MENU_KEYBOARD
    )
    await update.message.reply_text("🚀 Clique ici :", reply_markup=get_inline_keyboard())

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "Mon Compte" in text:
        await update.message.reply_text("👤 Mon Compte : Ouvre la Mini App pour voir ton solde et filleuls.", reply_markup=get_inline_keyboard())
    elif "Regarde une Pub" in text:
        await update.message.reply_text("📺 Regarde une Pub : 50F par pub, ouvre la Mini App :", reply_markup=get_inline_keyboard())
    elif "Inviter des Amis" in text:
        await update.message.reply_text("🔗 Inviter des Amis : 500F par ami, 5 min pour retirer. Ouvre la Mini App pour ton lien :", reply_markup=get_inline_keyboard())
    elif "Mes Tâches" in text:
        await update.message.reply_text("🚩 Mes Tâches :\n1️⃣ Rejoindre groupe privé (+100F)\n2️⃣ Inviter 5 amis (500F/ami)\nOuvre la Mini App :", reply_markup=get_inline_keyboard())
    elif "Retrait" in text:
        await update.message.reply_text("💵 Retrait : Conditions\n✅ Groupe rejoint\n✅ 5 filleuls\n✅ 30.000F\nOuvre la Mini App :", reply_markup=get_inline_keyboard())
    elif "Classement" in text:
        await update.message.reply_text("🏆 Classement : Bientôt disponible !")
    elif "Mini-Jeux" in text:
        await update.message.reply_text("🎮 Mini-Jeux : Bientôt !")
    elif "Procédure" in text:
        await update.message.reply_text("📋 Procédure :\n1. Regarde pub (50F)\n2. Rejoins groupe (100F)\n3. Invite 5 amis (500F/ami)\n4. Atteins 30.000F\n5. Retire via Wave")

@app.route('/')
def index():
    return HTML_MINI_APP

@app.route('/verif')
def verif():
    return '<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455"> OK'

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
