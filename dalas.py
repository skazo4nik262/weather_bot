#Запусти pipenv shell   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from dotenv import load_dotenv
import json
import os
import telebot
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from telebot import types

load_dotenv()

#bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
#omw_token = os.environ.get('OPEN_WEATHER_MAP_TOKEN')

owm_token = '527a29fa0c355edd16267f3b2d69ce52'
bot_token = '6637666670:AAEQLhIjaTQKLhqEcPmwEWNCZVJx0uqlY8Q'


bot = telebot.TeleBot(bot_token)
print("bot started")

config_dict = get_default_config()
config_dict['language'] = 'en'
owm = OWM(owm_token, config_dict)
mgr = owm.weather_manager()

@bot.message_handler(commands=['start'])
def start (message):
    user_name = message.from_user.user_name
    bot.reply_to(message, f'Приветствую, {user_name}! Чем могу быть поелзен?')
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Изменить город')
    btn2 = telebot.types.KeyboardButton('Узнать погоду')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Пожалуйста, выберите интересующий вас вариант:', reply_markup = markup)
@bot.message_handler(content_types=['text'])
def callback_message(message):
    if message.text == 'Изменить город':
        edit_city(message)
    elif message.text == 'Узнать погоду':
        weather(message)

@bot.message_handler(commands=['web'])
def web(message):
    try:
        city_name = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, 'Вы не указали город, пожалуйста введите город')
        return
    user_id = message.from_user.id
    with open('user_data.json') as file:
        data = json.load(file)
    data[(user_id)] = city_name

    with open ('user_data.json', 'w') as file:
        json.dump(data, file)
    bot.reply_to(message,"Ваш город сохранён")
def weather(city_name):
    owm = OWM(owm_token)
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(city_name)
        weather = observation.weather
        temp = weather.temperature('celsius')['temp']
        status = weather.detailed_status
        
    except:
        return
def weather(message):
    user_id = message.from_user.id
    with open('user_data.json') as file:
        data = json.load(file)
    city_name = data.get((user_id))
    if city_name:
        status, temp = weather(city_name)
        if status and temp:
            bot.send_message(message.chat.id, f'Сейчас в {city_name}: {status}, {temp}°C')
        else:
            bot.send_message(message.chat.id, 'Не удалось получить информацию о погоде')
    else:
        bot.send_message(message.chat.id, 'Вы не указали город')

def edit_city(message):
     bot.send_message(message.chat.id, 'Чтобы изменить город введите /web "Название города"(без кавычек)')

bot.polling(non_stop=True)
