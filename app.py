import os
import telebot
from flask import Flask, request, abort

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("No TOKEN env var")

TRACK_LINK = "https://vaybpro.notion.site/279d93a4b5ab80f089efc6369e54b9b6?pvs=105"
DONATE_LINK = "https://www.donationalerts.com/r/vayb_pro"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
app = Flask(__name__)

# --- клавиатуры ---
from telebot import types
def main_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
    kb.row(types.KeyboardButton("🎵 Прислать трек"))
    kb.row(types.KeyboardButton("🚀 Донат без очереди"))
    return kb

def back_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
    kb.row(types.KeyboardButton("⬅️ Назад"))
    return kb

# --- handlers ---
@bot.message_handler(commands=['start', 'menu'])
def start(m):
    bot.send_message(m.chat.id, "Выбери действие 👇", reply_markup=main_kb())

@bot.message_handler(func=lambda msg: msg.text == "🎵 Прислать трек")
def send_track(m):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Открыть форму 🎵", url=TRACK_LINK))
    bot.send_message(m.chat.id, "Залить трек можно здесь:", reply_markup=markup)
    bot.send_message(m.chat.id, "Нажми «Назад», чтобы вернуться 👇", reply_markup=back_kb())

@bot.message_handler(func=lambda msg: msg.text == "🚀 Донат без очереди")
def send_donate(m):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Задонатить 🚀", url=DONATE_LINK))
    bot.send_message(m.chat.id, "Поддержать проект можно здесь:", reply_markup=markup)
    bot.send_message(m.chat.id, "Нажми «Назад», чтобы вернуться 👇", reply_markup=back_kb())

@bot.message_handler(func=lambda msg: msg.text == "⬅️ Назад")
def back(m):
    bot.send_message(m.chat.id, "Главное меню 👇", reply_markup=main_kb())

@bot.message_handler(content_types=['text'])
def fallback(m):
    bot.send_message(m.chat.id, "Жми кнопку ниже 😉", reply_markup=main_kb())

# --- webhook endpoints ---
@app.route("/", methods=["GET"])
def index():
    return "ok", 200

@app.route(f"/{TOKEN}", methods=["POST"])
def receive_update():
    if request.headers.get("content-type") == "application/json":
        update = request.get_data().decode("utf-8")
        bot.process_new_updates([telebot.types.Update.de_json(update)])
        return "ok", 200
    else:
        abort(403)

# Установка webhook при старте (используем переменную окружения WEBHOOK_URL)
@app.before_first_request
def setup_webhook():
    webhook_url = os.getenv("WEBHOOK_URL")  # например, https://tg-bot-xxxx.onrender.com/<TOKEN>
    if webhook_url:
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)
        print("Webhook set to:", webhook_url)

# gunicorn будет искать переменную app
# запускать так: gunicorn app:app
