import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

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
<title>Cash Pub V4 - 30.000F</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script src="https://quge5.com/88/tag.min.js" data-zone="303312" async data-cfasync="false"></script>
<style>
*{{box-sizing:border-box}} body{{background:#0f1115;color:white;font-family:sans-serif;margin:0;padding:12px}}
.card{{background:#1a1f2e;border-radius:20px;padding:18px;margin-bottom:12px;border:1px solid #232a3d}}
.solde{{font-size:46px;font-weight:900;color:#4a7bff}} .solde-label{{color:#8a90a5;font-size:11px}}
.stats{{display:flex;gap:7px;margin-top:12px}} .stat{{background:#232a3d;border-radius:12px;padding:10px;flex:1;text-align:center}} .stat b{{display:block}} .stat span{{font-size:8px;color:#8a90a5}}
.btn-main{{background:linear-gradient(135deg,#4a7bff,#6a5cff);width:100%;padding:18px;border:none;border-radius:16px;color:white;font-size:17px;font-weight:900;margin:8px 0}}
.btn-task{{background:#1a2a1f;border:1px solid #2d6a4f;width:100%;padding:14px;border-radius:14px;color:#4ade80;font-size:14px;font-weight:bold;margin:6px 0;display:flex;justify-content:space-between;align-items:center}}
.btn-task.done{{background:#232a3d;color:#8a90a5;border-color:#232a3d}} .btn-sec{{background:#232a3d;width:100%;padding:14px;border:none;border-radius:14px;color:#8a90a5;font-size:14px;margin:6px 0}}
#pub-overlay{{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.95);z-index:999;flex-direction:column;align-items:center;justify-content:center;padding:20px;text-align:center}}
.timer{{font-size:90px;font-weight:900;color:#4a7bff}} .progress{{width:90%;height:10px;background:#232a3d;border-radius:10px;margin-top:15px;overflow:hidden}} .bar{{height:100%;background:#4a7bff;width:100%;transition:width 1s linear}}
.lock{{background:#2a1f1f;border:1px solid #6a2a2a;border-radius:14px;padding:12px;margin:10px 0;font-size:12px}}
</style>
</head>
<body>
<div id="pub-overlay">
  <div style="background:#4a7bff;color:white;padding:6px 12px;border-radius:20px;font-size:12px">PUB EN COURS</div>
  <div class="timer" id="count">30</div>
  <div>+50 F dans <span id="c2">30</span>s</div>
  <div class="progress"><div class="bar" id="bar"></div></div>
  <div style="font-size:11px;color:#8a90a5;margin-top:10px">2 pubs tournent - Double revenu</div>
</div>

<div style="display:flex;justify-content:space-between;padding:8px 4px"><b>💰 CASH PUB V4</b><span style="background:#232a3d;padding:5px 10px;border-radius:20px;font-size:11px">👥 <span id="par">0</span>/5 filleuls</span></div>

<div class="card">
  <div class="solde-label">SOLDE</div>
  <div class="solde" id="solde">0 F</div>
  <div class="stats">
    <div class="stat"><b id="total">0 F</b><span>TOTAL</span></div>
    <div class="stat"><b id="pubs">0</b><span>PUBS</span></div>
    <div class="stat"><b id="par2">0</b><span>FILLEULS</span></div>
  </div>
  <div id="lockInfo"></div>
</div>

<button class="btn-main" onclick="regarderPub()">▶ PUB • +50 F</button>

<div class="card">
  <div style="font-weight:bold;margin-bottom:10px">📋 TÂCHES OBLIGATOIRES (pour retirer)</div>
  <button class="btn-task" id="taskGroup" onclick="doTaskGroup()">
    <span>📢 Rejoindre le groupe privé</span><span id="tgText">+100 F >></span>
  </button>
  <button class="btn-task" id="taskInvite" onclick="invite()">
    <span>👥 Inviter 5 amis (500F / ami)</span><span id="invText">0/5</span>
  </button>
  <div style="font-size:10px;color:#8a90a5;margin-top:8px">Tu dois faire les 2 tâches + 30.000F pour retirer</div>
</div>

<button class="btn-sec" onclick="invite()">👥 Lien de parrainage • 500F / ami</button>
<button class="btn-sec" onclick="retirer()">💸 RETIRER • MIN 30.000F</button>

<div style="text-align:center;color:#5a627a;font-size:10px;margin-top:12px">Auto Vignette + Direct Link actif - Zone 303312</div>

<script>
let solde = parseInt(localStorage.getItem('solde')||'0');
let pubs = parseInt(localStorage.getItem('pubs')||'0');
let total = parseInt(localStorage.getItem('total')||'0');
let parrainages = parseInt(localStorage.getItem('parrainages')||'0');
let taskGroupDone = localStorage.getItem('taskGroupDone') === 'true';

const DIRECT_LINKS = ["https://uplcm.com/4/12147475","https://uplcm.com/4/12147480"];
const GROUP_LINK = "{GROUP_LINK}";

function refreshUI(){{
  document.getElementById('solde').innerText = solde+' F';
  document.getElementById('pubs').innerText = pubs;
  document.getElementById('total').innerText = total+' F';
  document.getElementById('par').innerText = parrainages;
  document.getElementById('par2').innerText = parrainages;
  document.getElementById('invText').innerText = parrainages+'/5';
  
  let lockDiv = document.getElementById('lockInfo');
  if(parrainages < 5 || solde < 30000 || !taskGroupDone){{
    lockDiv.innerHTML = `<div class="lock">🔒 Retrait bloqué:<br>
    ${{taskGroupDone?'✅':'❌'}} Groupe Telegram<br>
    ${{parrainages>=5?'✅':'❌'}} Parrainages: ${{parrainages}}/5<br>
    ${{solde>=30000?'✅':'❌'}} Solde: ${{solde}}/30000 F</div>`;
  }} else {{
    lockDiv.innerHTML = `<div style="background:#1e3a2e;border-radius:12px;padding:10px;margin-top:10px;color:#4ade80;font-size:12px">✅ Tu peux retirer !</div>`;
  }}
  
  if(taskGroupDone){{
    let btn = document.getElementById('taskGroup');
    btn.classList.add('done');
    document.getElementById('tgText').innerText = '✅ Fait';
  }}
  if(parrainages>=5){{
    document.getElementById('taskInvite').classList.add('done');
  }}
}}
refreshUI();

function doTaskGroup(){{
  if(taskGroupDone){{ alert("Déjà fait ✅"); return; }}
  window.open(GROUP_LINK, "_blank");
  setTimeout(()=>{{
    if(confirm("As-tu bien rejoint le groupe Telegram ? Clique OK pour recevoir 100F")){{
      taskGroupDone = true;
      solde+=100; total+=100;
      localStorage.setItem('taskGroupDone','true');
      localStorage.setItem('solde',solde);
      localStorage.setItem('total',total);
      refreshUI();
      alert("✅ +100 F ajouté ! Merci d'avoir rejoint le groupe !");
    }}
  }}, 3000);
}}

function regarderPub(){{
  window.open(DIRECT_LINKS[pubs % 2], "_blank");
  let overlay = document.getElementById('pub-overlay');
  overlay.style.display='flex';
  let count = 30;
  let timer = setInterval(()=>{{
    count--;
    document.getElementById('count').innerText = count;
    document.getElementById('c2').innerText = count;
    document.getElementById('bar').style.width = (count/30*100)+'%';
    if(count==15){{ window.open(DIRECT_LINKS[1], "_blank"); }}
    if(count<=0){{
      clearInterval(timer);
      overlay.style.display='none';
      solde+=50; pubs+=1; total+=50;
      if(pubs%10==0){{ solde+=100; alert("BONUS +100F"); }}
      localStorage.setItem('solde',solde); localStorage.setItem('pubs',pubs); localStorage.setItem('total',total);
      refreshUI();
      document.getElementById('count').innerText='30'; document.getElementById('bar').style.width='100%';
    }}
  }},1000);
}}

function invite(){{
  let refCode = localStorage.getItem('myRef') || Math.floor(Math.random()*90000+10000);
  localStorage.setItem('myRef', refCode);
  let link = "https://t.me/CashPubBot?start=ref_"+refCode;
  
  // Simulation: quand quelqu'un clique sur Inviter, on simule un filleul pour test
  // EN VRAI, tu devras vérifier via base de données
  if(navigator.share){{ navigator.share({{title:'Gagne 30.000F', text:'Rejoins moi et gagne 500F direct', url: link}}); }}
  else{{ prompt("Copie ton lien de parrainage (500F par ami):", link); }}
  
  // Pour tester vite: ajoute 1 filleul
  if(confirm("SIMULATION: Ajouter 1 filleul pour tester ? (En vrai, ce sera auto quand ton ami clique)")){{
    parrainages+=1; solde+=500; total+=500;
    localStorage.setItem('parrainages', parrainages);
    localStorage.setItem('solde', solde);
    localStorage.setItem('total', total);
    refreshUI();
    alert("🎉 Nouveau filleul ! +500 F");
  }}
}}

function retirer(){{
  if(!taskGroupDone){{ alert("❌ Tu dois d'abord rejoindre le groupe Telegram !\\nVa dans TÂCHES et clique sur Rejoindre"); return; }}
  if(parrainages < 5){{ alert("❌ Il te faut 5 filleuls minimum !\\nTu as: "+parrainages+"/5\\n\\nPartage ton lien !\\nTu gagnes 500F par ami"); return; }}
  if(solde < 30000){{ alert("❌ Solde insuffisant !\\nTu as: "+solde+" F / 30000 F\\nIl te manque: "+(30000-solde)+" F"); return; }}
  
  let num = prompt("✅ Bravo ! Conditions remplies:\\n✅ Groupe rejoint\\n✅ "+parrainages+"/5 filleuls\\n✅ "+solde+" F\\n\\nEntre ton numéro Wave / Orange Money:");
  if(num){{
    alert("✅ DEMANDE ENVOYÉE !\\nNuméro: "+num+"\\nMontant: "+solde+" F\\nTu seras payé dans 24h");
    solde=0; localStorage.setItem('solde',0); refreshUI();
  }}
}}

// Gestion vrai parrainage via URL ?start=ref_XXXX
const urlParams = new URLSearchParams(window.location.search);
let ref = urlParams.get('tgWebAppStartParam') || urlParams.get('start');
if(ref && ref.includes('ref_')){{
  if(!localStorage.getItem('alreadyReferred')){{
    localStorage.setItem('alreadyReferred','true');
    // Ici on devrait envoyer au backend pour créditer le parrain
    console.log("Nouveau filleul détecté:", ref);
  }}
}}

Telegram.WebApp.ready(); Telegram.WebApp.expand();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_MINI_APP

@app.route('/verif')
def verif():
    return '<meta name="monetag" content="3d6f80bc1545f19f62998e82de8b3455"> OK'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Récupère le ref si présent
    args = context.args
    ref_text = ""
    if args:
        ref_text = f"\\n\\n🎁 Invité par: {args[0]} - Tu reçois 500F de bonus !"
    
    kb = [[InlineKeyboardButton("💰 Ouvrir Cash Pub V4", web_app=WebAppInfo(url=WEBAPP_URL))],
          [InlineKeyboardButton("📢 Rejoindre le groupe", url=GROUP_LINK)]]
    
    await update.message.reply_text(
        f"🔥 CASH PUB V4 - NOUVEAU 🔥{ref_text}\n\n"
        "💰 50 F par pub (30s)\n"
        "👥 500 F par ami parrainé\n"
        "📢 100 F pour rejoindre le groupe\n"
        "🎁 Bonus 100F tous les 10 pubs\n"
        "💸 Retrait à 30.000 F\n\n"
        "🔒 CONDITIONS RETRAIT:\n"
        "✅ Rejoindre groupe Telegram\n"
        "✅ 5 filleuls minimum\n"
        "✅ 30.000 F de solde\n\n"
        "3 revenus Monetag actifs !",
        reply_markup=InlineKeyboardMarkup(kb)
    )

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

def run_bot_fix():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot_fix()
