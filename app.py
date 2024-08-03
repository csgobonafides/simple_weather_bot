import telebot              #Установленый из pypi
import requests
import json

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

class BotConfig(BaseSettings):
    token: str

    class Config:
        env_file = '.env'
        env_prefix = 'BOT_'

load_dotenv()
config = BotConfig()
bot = telebot.TeleBot(config.token)
# bot = telebot.TeleBot('7000620374:AAHUp-ttpGXBumF6nGHbeLF3uA1K4Z4RigU') #токен бота
api = '9b6ad82f21abd4ed6e636e6674de6b1c'

@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Погода в каком городе вас интересует?')
    print(message.text.strip().lower())

# @bot.message_handler(content_types=['text'])
@bot.message_handler(commands=['п'])
def get_weather(message):
    mess = message.text.strip().lower()
    get_city = mess.split()
    if len(get_city) == 2 and get_city[0].lower() == '/п':
        city = get_city[1]
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric')
        if res.status_code == 200:
            data = json.loads(res.text)
            sky = data['weather'][0]['main']
            emods = None
            if sky == 'Clouds':
                emods = '☁️ Облачно'
            elif sky == 'Snow':
                emods = '❄️ Снег'
            elif sky == 'Clear':
                emods = '🌞 Ясно'
            elif sky == 'Rain':
                emods = '🌧️️ Дождь'
            else:
                emods = 'Что-то новенькое 🤔'
            bot.reply_to(message, f"Температура в городе {data['name']}: {int(data['main']['temp'])}℃ {emods}.")
        else:
            bot.reply_to(message, 'Название города введено не коректно.')

@bot.message_handler(commands=['л'])
def get_weather(message):
    mess = message.text.strip().lower()
    get_city = mess.split()
    if len(get_city) == 2 and get_city[0].lower() == '/л':
        city = get_city[1]
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric')
        if res.status_code == 200:
            data = json.loads(res.text)
            bot.reply_to(message, f"Люблю город {data['name']} 💘💘💘")
        else:
            bot.reply_to(message, 'Странные у вас предпочтения.')



bot.polling(none_stop=True)