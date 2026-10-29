import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = "https://cash-pub-bot.onrender.com"
GROUP_LINK = "https://t.me/+TH2UW0jyWthlM2U0"

app = Flask(__name__)

HTML_MINI_APP = f"""
<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455">
<title>Cash Pub V7</title><script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="https://quge5.com/88/tag.min.js" data-zone="303312" async data-cfasync="false"></script>
<style>*{{box-sizing:border-box}}body{{background:#0f1115;color:#fff;font-family:Arial,sans-serif;margin:0;padding:12px}} .card{{background:#1a1f2e;border-radius:20px;padding:18px;margin-bottom:12px;border:1px solid #232a3d}} .solde{{font-size:48px;font-weight:900;color:#4a7bff}} .btn-main{{background:linear-gradient(135deg,#4a7bff,#6a5cff);width:100%;padding:18px;border:none;border-radius:16px;color:white;font-size:18px;font-weight:900;margin:8px 0;cursor:pointer}} .btn-task{{background:#1a2a1f;border:1px solid #2d6a4f;width:100%;padding:14px;border-radius:14px;color:#4ade80;font-size:14px;font-weight:bold;margin:6px 0;display:flex;justify-content:space-between}} .btn-task.done{{background:#232a3d;color:#8a90a5}} .btn-sec{{background:#232a3d;width:100%;padding:14px;border:none;border-radius:14px;color:#8a90a5;margin:6px 0}} #pub-overlay{{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.95);z-index:999;flex-direction:column;align-items:center;justify-content:center;padding:20px}} .timer{{font-size:90px;font-weight:900;color:#4a7bff}} .progress{{width:90%;height:10px;background:#232a3d;border-radius:10px;margin-top:15px;overflow:hidden}} .bar{{height:100%;background:#4a7bff;width:100%}} .lock{{background:#2a1f1f;border:1px solid #6a2a2a;border-radius:14px;padding:12px;margin:10px 0;font-size:12px;line-height:1.6}}</style>
</head><body>
<div id="pub-overlay"><div class="timer" id="count">30</div><div>+50 F dans <span id="c2">30</span>s</div><div class="progress"><div class="bar" id="bar"></div></div></div>
<div style="display:flex;justify-content:space-between;padding:8px 4px"><b>💰 CASH PUB V7</b><span style="background:#232a3d;padding:5px 10px;border-radius:20px;font-size:11px">👥 <span id="par">0</span>/5</span></div>
<div class="card"><div style="color:#8a90a5;font-size:11px">TON SOLDE</div><div class="solde" id="solde">0 F</div><div style="display:flex;gap:7px;margin-top:12px"><div style="background:#232a3d;border-radius:12px;padding:10px;flex:1;text-align:center"><b id="total">0</b><br><span style="font-size:8px">TOTAL GAGNÉ</span></div><div style="background:#232a3d;border-radius:12px;padding:10px;flex:1;text-align:center"><b id="pubs">0</b><br><span style="font-size:8px">PUBS VUES</span></div><div style="background:#232a3d;border-radius:12px;padding:10px;flex:1;text-align:center"><b id="par2">0</b><br><span style="font-size:8px">FILLEULS</span></div></div><div id="lockInfo"></div></div>
<button class="btn-main" onclick="regarderPub()">▶ REGARDER UNE PUB • +50 F</button>
<div class="card"><b>📋 TÂCHES OBLIGATOIRES POUR RETRAIT</b><button class="btn-task" id="taskGroup" onclick="doTaskGroup()"><span>📢 Rejoindre groupe privé (obligatoire)</span><span id="tgText">+100 F >></span></button><button class="btn-task" onclick="invite()"><span>👥 Inviter 5 amis (500F / ami)</span><span id="invText">0/5</span></button><button class="btn-task"><span>💰 Atteindre 30.000 F</span><span id="soldeTask">0/30000</span></button></div>
<button class="btn-sec" onclick="invite()">🔗 Mon Lien Parrainage - 500F/ami</button><button class="btn-sec" onclick="retirer()">💵 DEMANDER RETRAIT 30.000F</button>
<script>
let solde=parseInt(localStorage.getItem('solde')||'0');let pubs=parseInt(localStorage.getItem('pubs')||'0');let total=parseInt(localStorage.getItem('total')||'0');let parrainages=parseInt(localStorage.getItem('parrainages')||'0');let taskGroupDone=localStorage.getItem('taskGroupDone')==='true';const DIRECT_LINKS=["https://uplcm.com/4/12147475","https://uplcm.com/4/12147480"];const GROUP_LINK="{GROUP_LINK}";
function refreshUI(){{document.getElementById('solde').innerText=solde+' F';document.getElementById('pubs').innerText=pubs;document.getElementById('total').innerText=total+' F';document.getElementById('par').innerText=parrainages;document.getElementById('par2').innerText=parrainages;document.getElementById('invText').innerText=parrainages+'/5';document.getElementById('soldeTask').innerText=solde+'/30000';let lockDiv=document.getElementById('lockInfo');if(parrainages<5||solde<30000||!taskGroupDone){{lockDiv.innerHTML=`<div class="lock">🔒 RETRAIT BLOQUÉ:<br>${{taskGroupDone?'✅':'❌'}} Groupe privé<br>${{parrainages>=5?'✅':'❌'}} Parrainages: ${{parrainages}}/5<br>${{solde>=30000?'✅':'❌'}} Solde: ${{solde}}/30000 F</div>`;}}else{{lockDiv.innerHTML=`<div style="background:#1e3a2e;border-radius:12px;padding:10px;margin-top:10px;color:#4ade80;font-size:12px">✅ BRAVO ! Tu peux retirer tes ${{solde}} F !</div>`;}}if(taskGroupDone){{document.getElementById('taskGroup').classList.add('done');document.getElementById('tgText').innerText='✅ Fait +100F';}}}}
refreshUI();
function doTaskGroup(){{if(taskGroupDone){{alert("Déjà fait ✅");return;}}window.open(GROUP_LINK,"_blank");setTimeout(()=>{{if(confirm("As-tu rejoint le groupe privé ? Clique OK pour +100F")){{taskGroupDone=true;solde+=100;total+=100;localStorage.setItem('taskGroupDone','true');localStorage.setItem('solde',solde);localStorage.setItem('total',total);refreshUI();}}}},2000);}}
function regarderPub(){{window.open(DIRECT_LINKS[pubs%2],"_blank");let overlay=document.getElementById('pub-overlay');overlay.style.display='flex';let count=30;let timer=setInterval(()=>{{count--;document.getElementById('count').innerText=count;document.getElementById('c2').innerText=count;document.getElementById('bar').style.width=(count/30*100)+'%';if(count==15){{window.open(DIRECT_LINKS[1],"_blank");}}if(count<=0){{clearInterval(timer);overlay.style.display='none';solde+=50;pubs+=1;total+=50;localStorage.setItem('solde',solde);localStorage.setItem('pubs',pubs);localStorage.setItem('total',total);refreshUI();}}}},1000);}}
function invite(){{let refCode=localStorage.getItem('myRef')||Math.floor(Math.random()*90000+10000);localStorage.setItem('myRef',refCode);let link="https://t.me/GainsFacilesCI_bot?start=ref_"+refCode;prompt("Copie ton lien parrainage (500F par ami):",link);}}
function retirer(){{if(!taskGroupDone){{alert("❌ Tu dois d'abord rejoindre le groupe privé");return;}}if(parrainages<5){{alert("❌ Il faut 5 filleuls, tu as "+parrainages+"/5");return;}}if(solde<30000){{alert("❌ Solde insuffisant: "+solde+"/30000 F. Regarde des pubs et invite des amis !");return;}}let num=prompt("Entre ton numéro Wave / MTN / Orange pour recevoir "+solde+" F:");if(num){{alert("✅ Demande de retrait envoyée !\\n\\nMontant: "+solde+" F\\nNuméro: "+num+"\\n\\nPaiement sous 24h-48h");solde=0;localStorage.setItem('solde',0);refreshUI();}}}}
Telegram.WebApp.ready();Telegram.WebApp.expand();
</script></body></html>
"""

# CLAVIER ANCIEN + NOUVEAU
MENU_KEYBOARD = ReplyKeyboardMarkup([
    ["👤 Mon Compte","📺 Regarde une Pub"],
    ["🔗 Inviter des Amis","🚩 Mes Tâches"],
    ["💵 Retrait","🏆 Classement"],
    ["🎮 Mini-Jeux","📋 Procédure"]
], resize_keyboard=True)

def get_inline_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 OUVRIR LA MINI APP (V7)", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("📢 Rejoindre le groupe privé", url=GROUP_LINK)]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenue sur Gains Faciles CI - V7 !\n\n"
        "💰 50F par pub\n"
        "👥 500F par filleul\n"
        "📢 100F groupe privé\n"
        "💸 Retrait à 30.000F (5 filleuls)\n\n"
        "👇 Utilise le menu en bas :",
        reply_markup=MENU_KEYBOARD
    )
    await update.message.reply_text("🚀 Clique pour ouvrir ton app :", reply_markup=get_inline_keyboard())

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text
    if "Mon Compte" in txt:
        await update.message.reply_text("👤 MON COMPTE\n\nOuvre la Mini App pour voir ton solde, tes pubs, tes filleuls.\nConditions retrait: Groupe + 5 amis + 30.000F", reply_markup=get_inline_keyboard())
    elif "Regarde" in txt:
        await update.message.reply_text("📺 REGARDER UNE PUB = +50F\nOuvre la Mini App et clique sur PUB", reply_markup=get_inline_keyboard())
    elif "Inviter" in txt:
        await update.message.reply_text("🔗 INVITER DES AMIS = 500F / ami\n\n5 filleuls minimum pour retirer.\nTon lien est dans la Mini App.", reply_markup=get_inline_keyboard())
    elif "Tâches" in txt:
        await update.message.reply_text("🚩 MES TÂCHES:\n1. Rejoindre groupe privé = +100F (obligatoire)\n2. Inviter 5 amis = 2500F\n3. Atteindre 30.000F\n\nTout est dans la Mini App.", reply_markup=get_inline_keyboard())
    elif "Retrait" in txt:
        await update.message.reply_text("💵 RETRAIT 30.000F:\n✅ Groupe privé rejoint\n✅ 5 filleuls\n✅ 30.000F solde\n\nFais ta demande dans la Mini App.", reply_markup=get_inline_keyboard())
    elif "Classement" in txt:
        await update.message.reply_text("🏆 CLASSEMENT:\n1. @user1 - 125.000F\n2. @user2 - 98.000F\n3. @user3 - 75.000F\n\nContinue d'inviter pour être top !", reply_markup=get_inline_keyboard())
    elif "Mini-Jeux" in txt:
        await update.message.reply_text("🎮 MINI-JEUX bientôt ! Pour l'instant gagne avec Pubs + Parrainage.", reply_markup=get_inline_keyboard())
    elif "Procédure" in txt:
        await update.message.reply_text("📋 PROCÉDURE:\n1. Regarde des pubs (50F)\n2. Rejoins groupe privé (100F)\n3. Invite 5 amis (500F/ami)\n4. Atteins 30.000F\n5. Demande retrait Wave", reply_markup=get_inline_keyboard())
    else:
        await update.message.reply_text("Ouvre la Mini App V7 :", reply_markup=get_inline_keyboard())

@app.route('/')
def index(): return HTML_MINI_APP

@app.route('/verif')
def verif(): return '<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455"> Verif OK'

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
