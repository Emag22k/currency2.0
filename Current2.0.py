from locale import currency
from math import lgamma

import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot=telebot.TeleBot("7895887660:AAEUZg_HL5s957m8pqTGXCcrorx3b0BoRR8")
curr=CurrencyConverter()
amount=0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я помогу тебе с валютами\n'
                                      'Введи сумму: ')

    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount=int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Впишите сумму")
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup=types.InlineKeyboardMarkup(row_width=2)
        btn1=types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
        btn2=types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
        btn3=types.InlineKeyboardButton("USD/GBP", callback_data="usd/gbp")
        btn4=types.InlineKeyboardButton("GBP/USD", callback_data="gbp/usd")
        btn5=types.InlineKeyboardButton("Другие значения", callback_data="else")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, "Выберите пару валют",reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Неверный формат. Число должно быть больше 0")

        bot.register_next_step_handler(message,summa)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data != "else":
        values=call.data.upper().split('/')
        res= curr.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res,2)},что еще посчитать?')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Введите пару значений через слэш")
        bot.register_next_step_handler(call.message, user_curr)

def user_curr(message):
    try:
        values = message.data.upper().split('/')
        res = curr.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)},что еще посчитать?')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Хм.Что-то не так. Впишите значение снова')
        bot.register_next_step_handler(message, user_curr)



bot.polling(non_stop=True)