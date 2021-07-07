import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.token)

def admin_button(message):
    pass


@bot.message_handler(commands=['start'])
def welcome(message):
    if message.chat.id == config.test_id:
        admin_button(message)

    else:
        button = types.ReplyKeyboardMarkup(True, True)
        button.row('Да, заказать!')

        bot.send_message(message.chat.id, 'Привет! На связи ЗЛАКИ МАКИ! Хочешь подкрепиться?', reply_markup=button)
