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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Изменить город")
    btn2 = types.KeyboardButton("Узнать погоду")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, f'Приветсвую, {message.from_user.first_name}! Чтобы узнать погоду в городе, просто напишите название города. Если вы хотите сохранить свой город, чтобы постоянно не вводить его название, то нажмите на конпку "Изменить город" для полуения большей информации', reply_markup=markup)



@bot.message_handler(commands=['save'])
def split(message):
     #Привидение сообщения в список, выявление названия города
    try:
        splited_message = message.text
        splited_message = splited_message.split(" ")
        splited_message = splited_message[1:]
        city = " ".join (splited_message)
        print(city)
    except Exception as e:
        bot.reply_to(message, "Вы не указали город")
    
    #Получение айди пользователя и его последнего сообщения
    user_id = message.from_user.id
    user_data[user_id] = city
    
    #Запись города в json
    with open('user_data.json', 'w') as file:
         json.dump(user_data, file)
    print(f"Ваш город: {city} сохранён")
    bot.reply_to(message, f"Ваш город: {city} сохранён")
    


@bot.message_handler(commands=['weather'])
def weather(message):
    with open('user_data.json', 'r') as file:
        user_data = json.load(file)
    user_id = str(message.from_user.id)
    if user_id in user_data:
        city = user_data[user_id]
        print(f'Ваш город: {city}')
    try:
            observation = mgr.weather_at_place(city)
            weather = observation.weather
            temp = weather.temperature('celsius')['temp']
            status = weather.detailed_status
            bot.send_message(message.chat.id, f'В городе {city} сейчас: {status}, {temp}')
    except Exception as e:
            bot.send_message(message.chat.id, 'К сожалению вашего города нет в нашей базе')



@bot.message_handler(content_types=['text'])
def weather2(message):
    city = message.text
    try:
            observation = mgr.weather_at_place(city)
            weather = observation.weather
            temp = weather.temperature('celsius')['temp']
            status = weather.detailed_status
            bot.send_message(message.chat.id, f'В городе {city} сейчас: {status}, {temp}')
    except Exception as e:
            bot.send_message(message.chat.id, 'К сожалению вашего города нет в нашей базе')


#Функционал кнопок
@bot.message_handler(content_types=['text'])
def button(message):
    if message.text == 'Изменить город':
        bot.send_message(message.chat.id, "Чтобы сохранить город напишите: /save 'Название города'(без кавычек)")
    elif message.text == 'Узнать погоду':
        weather(message)
    

bot.polling(none_stop=True)
