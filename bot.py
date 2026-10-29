import os
from flask import Flask
import threading
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎉 Ton bot Gains Faciles CI est en ligne 24/24 ! Bienvenue Jean !")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

@app.route('/')
def home():
    return "Bot Cash Pub CI en ligne !"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
