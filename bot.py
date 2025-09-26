import telebot
from telebot import types

TOKEN = "8244287234:AAGxP2L6wthn-tWeBDZlekWclvXbBISQpBc"
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ссылки
TRACK_LINK = "https://vaybpro.notion.site/279d93a4b5ab80f089efc6369e54b9b6?pvs=105"
DONATE_LINK = "https://www.donationalerts.com/r/vayb_pro"

# --- клавиатуры ---
def main_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
    kb.row(types.KeyboardButton("🎵 Прислать трек"))
    kb.row(types.KeyboardButton("🚀 Донат без очереди"))
    return kb

def back_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
    kb.row(types.KeyboardButton("⬅️ Назад"))
    return kb

# --- обработчики ---
@bot.message_handler(commands=['start', 'menu'])
def start(m):
    bot.send_message(m.chat.id, "Выбери действие 👇", reply_markup=main_kb())

# меню «Прислать трек»
@bot.message_handler(func=lambda msg: msg.text == "🎵 Прислать трек")
def send_track(m):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Открыть форму 🎵", url=TRACK_LINK))
    bot.send_message(m.chat.id, "Залить трек можно здесь:", reply_markup=markup)
    bot.send_message(m.chat.id, "Нажми «Назад», чтобы вернуться 👇", reply_markup=back_kb())

# меню «Донат»
@bot.message_handler(func=lambda msg: msg.text == "🚀 Донат без очереди")
def send_donate(m):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Задонатить 🚀", url=DONATE_LINK))
    bot.send_message(m.chat.id, "Поддержать проект можно здесь:", reply_markup=markup)
    bot.send_message(m.chat.id, "Нажми «Назад», чтобы вернуться 👇", reply_markup=back_kb())

# кнопка «Назад»
@bot.message_handler(func=lambda msg: msg.text == "⬅️ Назад")
def back(m):
    bot.send_message(m.chat.id, "Главное меню 👇", reply_markup=main_kb())

# всё остальное
@bot.message_handler(content_types=['text'])
def fallback(m):
    bot.send_message(m.chat.id, "Жми кнопку ниже 😉", reply_markup=main_kb())

print("Бот запущен!")
bot.infinity_polling()
