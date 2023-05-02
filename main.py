import os

import telebot
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_key = os.environ.get("API")
bot_key = os.environ.get("BOT")


bot = telebot.TeleBot(bot_key)
API = API_key


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'введите город')


@bot.message_handler(content_types=['text'])
def get_text(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = res.json()
        temp = data["main"]["temp"]
        bot.send_message(message.chat.id, f'сейчас: {temp}')
        image = 'cold.jpeg' if temp < 5.0 else 'hott.jpeg'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, 'город указан не верно')


bot.polling(none_stop=True)
