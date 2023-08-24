#Запусти pipenv shell   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from dotenv import load_dotenv
import json
import os
import telebot
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from telebot import types

load_dotenv()

#Запуск бота
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
omw_token = os.environ.get('OPEN_WEATHER_MAP_TOKEN')

bot = telebot.TeleBot(bot_token)
print("Бот запущен")

user_data = {}

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM(omw_token, config_dict)
mgr = owm.weather_manager()

#Ответ на команду /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Приветсвую, {message.from_user.first_name}! Чем могу быть полезен?')

#Ответ на команду /web
@bot.message_handler(commands=['web', 'site', 'website', 'weathersite'])
def site(message):
    global user_data
#Привидение сообщения в список, выявление названия города
    splited_message = message.text.split(" ")
    city = " ".join (splited_message[1:])

#Проверка пустой строки
    try:
            print (city)
            observation = mgr.weather_at_place(city)
            weather = observation.weather
            temp = weather.temperature('celsius')['temp']
            status = weather.detailed_status
            bot.send_message(message.chat.id, f'В городе {city} сейчас: {status}, {temp}')
    except Exception as e:
            bot.send_message(message.chat.id, f'Укажите город в котором хотите посмотреть погоду')    

          
    else:

    
        bot.reply_to(message, "Ваш город сохранён")

#Получение айди пользователя и его последнего сообщения
    user_id = message.from_user.id
    user_data[user_id] = city

#Запись города в json          
    with open('user_data.json', 'w') as file:
         json.dump(user_data, file)
    

#Ответ на команду /weather с использование города из json
@bot.message_handler(commands = ['weather']) 
def get_saved_data(message):
    global user_data
    user_id = message.from_user.id
    

#Использование данных из json
    if user_id in user_data:
        saved_data = user_data[user_id]
        print(saved_data)

    with open('user_data.json', 'r') as file:
        user_data = json.load(file)
        bot.reply_to(message, 'Ваш город', {saved_data})










#Всегда запущен
bot.polling(none_stop=True)