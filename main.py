import telebot

from config import *
from extensions import Converter, ApiException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Приветствие!"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, sym, amount = message.text.split()
    except ValueError as e:
        bot.reply_to(message, "неверное количество параметров")

    try:
        new_price = Converter.get_price(base, sym, amount)
        bot.reply_to(message, F"цена {amount} {base} в {sym}:{new_price}")
    except ApiException as e:
        bot.reply_to(message, f"ошибка в команде: \n{e}" )

bot.polling()