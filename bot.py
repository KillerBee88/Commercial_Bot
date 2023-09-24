import os
# import random
import telebot
# import schedule
# import time
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('TG_BOT_TOKEN')

bot = telebot.TeleBot(bot_token)

states = {}


def post_message(number):
    if number > 28:
        number = 1

    text_file = f'texts/text_{number}.txt'
    with open(text_file, 'r', encoding='utf-8') as file:
        post_text = file.read()

    media_file = f'media/media_{number}.mp4' if os.path.exists(
        f'media/media_{number}.mp4') else f'media/media_{number}.jpg'

    try:
        if media_file.endswith('.jpg'):
            bot.send_photo('@krasota_vdetalyakh',
                           open(media_file, 'rb'), caption=post_text)
        elif media_file.endswith('.mp4'):
            bot.send_video('@krasota_vdetalyakh',
                           open(media_file, 'rb'), caption=post_text)
        print(f'Пост {number} опубликован в канале')
    except Exception as e:
        print(f'Ошибка при публикации поста {number}: {str(e)}')


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message, "Привет! Я бот для постинга сообщений. Пожалуйста, введите номер поста:")
    states[message.chat.id] = 'awaiting_post_number'


@bot.message_handler(func=lambda message: states.get(message.chat.id) == 'awaiting_post_number')
def process_post_number(message):
    try:
        number = int(message.text)
        post_message(number)
        bot.reply_to(message, f"Пост номер {number} опубликован в канале.")
        states[message.chat.id] = 'awaiting_post_number'
    except ValueError:
        bot.reply_to(
            message, "Неверный формат номера поста. Пожалуйста, введите число.")


bot.polling()
