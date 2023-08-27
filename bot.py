#Запусти pipenv shell   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from dotenv import load_dotenv
import json
import os
import telebot
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from telebot import types

load_dotenv()

bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
omw_token = os.environ.get('OPEN_WEATHER_MAP_TOKEN')

bot = telebot.TeleBot(bot_token)
print("bot started")

config_dict = get_default_config()
config_dict['language'] = 'en'
owm = OWM(omw_token, config_dict)
mgr = owm.weather_manager()

user_data = {}

#/web
@bot.message_handler(commands=['web'])
def city(message):
    splited_message = message.text
    splited_message = splited_message.split(" ")
    splited_message = splited_message[1:]
    city = " ".join (splited_message)
    print(city)
    try:
            observation = mgr.weather_at_place(city)
            weather = observation.weather
            temp = weather.temperature('celsius')['temp']
            status = weather.detailed_status
            # city & id w to json
            with open('user_data.json', 'w') as file:
                json.dump(user_data, file) 
    except Exception as e:
            bot.send_message(message.chat.id, 'Укажите город, в котором вы хотите посмотреть погоду')
    else:
        bot.reply_to(message, "Ваш город сохранён")


   

#/start
@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Изменить город")
    btn2 = types.KeyboardButton("Узнать погоду")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, f'Приветсвую, {message.from_user.username}! Чем могу быть полезен?', reply_markup=markup)
    
    #btn1 & btn2
@bot.message_handler(content_types=['text'])
def callback_message(message):
    if message.text == 'Изменить город':
        edit_city(message)
    elif message.text == 'Узнать погоду':
        weather(message)

#edit city
def edit_city(message):
     bot.send_message(message.chat.id, 'Чтобы изменить город введите /web "Название города"(без кавычек)')
     

# weather
def weather(message):
    with open('user_data.json', 'r') as file:
        user_data = json.load(file)
        user_id = str(message.from_user.id) 

        if user_id in user_data:
            observation = mgr.weather_at_place(city)
            weather = observation.weather
            temp = weather.temperature('celsius')['temp']
            status = weather.detailed_status
            city = user_data[user_id]
            bot.send_message(message.chat.id, f'В городе {city} сейчас: {status}, {temp}')
        else:
            bot.reply_to(message, 'Вы не указали  город')


#Всегда запущен
bot.polling(none_stop=True)
