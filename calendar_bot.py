import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import calendar
from datetime import datetime

TOKEN = "8576476633:AAFDcSvp82YIx6jwwG6uSd9pueWaDBzsbV0"

bot = telebot.TeleBot(TOKEN)

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "📅 Calendar botga xush kelibsiz!\n\n/calendar — kalendarni ochish"
    )

# /calendar
@bot.message_handler(commands=['calendar'])
def show_calendar(message):
    now = datetime.now()
    send_calendar(message.chat.id, now.year, now.month)

def send_calendar(chat_id, year, month):
    markup = InlineKeyboardMarkup(row_width=7)
    cal = calendar.monthcalendar(year, month)

    # Oy nomi
    markup.add(InlineKeyboardButton(f"{calendar.month_name[month]} {year}", callback_data="ignore"))

    # Haftaning kunlari
    days = ["Du", "Se", "Ch", "Pa", "Ju", "Sh", "Ya"]
    markup.add(*[InlineKeyboardButton(d, callback_data="ignore") for d in days])

    # Kunlar
    for week in cal:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data="ignore"))
            else:
                row.append(
                    InlineKeyboardButton(
                        str(day),
                        callback_data=f"day_{day}_{month}_{year}"
                    )
                )
        markup.add(*row)

    bot.send_message(chat_id, "📅 Kunni tanlang:", reply_markup=markup)

# Tugma bosilganda
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "ignore":
        bot.answer_callback_query(call.id)
        return

    if call.data.startswith("day_"):
        _, day, month, year = call.data.split("_")
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            f"📌 Siz tanladingiz: {day}.{month}.{year}"
        )

bot.polling(none_stop=True)
