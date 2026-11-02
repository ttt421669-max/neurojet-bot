import os
from flask import Flask
from google import genai
import telebot

TOKEN = os.environ.get("TG_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

app = Flask(__name__)


@app.route("/")
def index():
  return "NeuroJet Bot is running!"


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  bot.reply_to(
      message,
      "Привіт! Я ваш Telegram-бот на базі Google Gemini. Напишіть мені"
      " що-небудь!",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=message.text
    )
    bot.reply_to(message, response.text)
  except Exception as e:
    bot.reply_to(message, f"Сталася помилка: {e}")


if __name__ == "__main__":
  import threading

  bot_thread = threading.Thread(target=bot.infinity_polling)
  bot_thread.daemon = True
  bot_thread.start()

  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)
  
