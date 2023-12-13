#!/usr/bin/python
import telebot
import os
from dotenv import load_dotenv
from db_utils import get_file_id, add_file_id
from utils import get_picture


load_dotenv()
token = os.environ.get('token')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    file_id = get_file_id('greetings.jpg')
    if not file_id:
        picture = get_picture('greetings.jpg')
        msg = bot.send_photo(message.chat.id, picture)
        add_file_id('greetings.jpg', msg.photo[-1].file_id)
    else:
        msg = bot.send_photo(message.chat.id, file_id)
    bot.send_message(message.chat.id, "Дратути?")


@bot.message_handler(content_types=['text'])
def process_messages(message):
    bot.send_message(message.chat.id, message.text)


def start():
    bot.infinity_polling()


if __name__ == '__main__':
    start()
