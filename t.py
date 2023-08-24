#Запусти pipenv shell   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from dotenv import load_dotenv

import json
import os
import telebot
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
import webbrowser
from telebot import types
load_dotenv()
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
omw_token = os.environ.get('OPEN_WEATHER_MAP_TOKEN')
bot = telebot.TeleBot(bot_token)
print("Бот запущен")
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM(omw_token, config_dict)
mgr = owm.weather_manager()
user_data = {}




@bot.message_handler(commands=['web', 'site', 'website', 'weathersite'])
def site(message):
    global user_data
    #Привидение сообщения в список, выявление названия города
    splited_message = message.text
    splited_message = splited_message.split(" ")
    splited_message = splited_message[1:]
    city = " ".join (splited_message)

    #if not city:
     #       bot.send_message(message.chat.id, 'Укажите город в котором хотите посмотреть погоду. Например, /web Москва или /web Moscow' ) 
    try:
            print (city)
            observation = mgr.weather_at_place(city)
            weather = observation.weather
            temp = weather.temperature('celsius')['temp']
            status = weather.detailed_status
            bot.send_message(message.chat.id, f'В городе {city} сейчас: {status}, {temp}')
    except Exception as e:
            bot.send_message(message.chat.id, f'Укажите город в котором хотите посмотреть погоду')    

    #Получение айди пользователя и его последнего сообщения
    user_id = message.from_user.id
    last_city = city
    user_data[user_id] = last_city

    with open(json_file_path, 'w') as file:
         json.dump(user_data, file)
    
    bot.reply_to(message, "Ваш город сохранён")


@bot.message_handler(commands = ['weather']) 
def get_saved_data(message): 
     global user_data  
     with open ('user_data.json', 'r') as file:
         user_data = json.load(file)
         user_id = user_data['user_id']
         last_message = user_data ['last_message']

     if message.from_user.id in user_data:
         saved_data = user_data[message.from_user.id]
         print(user_data)










#Ответ на команду /info
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, message)
#Ответ на команду /start
#@bot.message_handler(commands=['start'])
#def start(message):
#    bot.send_message(message.chat.id, f'Приветсвую, {message.from_user.first_name}! Чем могу быть полезен?')

#Ответ с ссылкой на фото
@bot.message_handler(content_types=['photo'])
def get_photo(message):
     bot.reply_to(message, 'nice photo')

#Ответ с ссылкой на видео
@bot.message_handler(content_types=['video'])
def get_video(message):
    bot.reply_to(message, 'nice video')



def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, 'web is open')
    elif message.text == 'Удалить аудио' :
        bot.send_message(message.chat.id, 'deleted')

#Ответ с отсылкой на аудио(не на гс)
@bot.message_handler(content_types=['audio'])
def get_audio(message):

    markup = types.InlineKeyboardMarkup()
    
    btn1 = types.InlineKeyboardButton('перейти на сайт', url='https://gismeteo.ru')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('удалить аудио', callback_data='delete')
    
    btn3 = types.InlineKeyboardButton('редактировать текст', callback_data='edit')
    markup.row(btn2, btn3)
    
    bot.reply_to(message, 'nice audio', reply_markup=markup)

#Функционал кнопок 2 и 3
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id )

@bot.message_handler(commands=['start'])
def start(message):
     #добавление кнопок по парядку по одной в ряд
     #markup.add(types.ReplyKeyboardButton('Перейти на сайт'))

    markup = types.ReplyKeyboardMarkup()

    btn5 = types.KeyboardButton('Перейти на сайт')
    btn6 = types.KeyboardButton('Удалить аудио')
    markup.row(btn5, btn6)
    btn7 = types.KeyboardButton('Редактировать текст')
    markup.row(btn7)













































@bot.message_handler()
def main(message):
    if message.text.lower() =='id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
    elif message.text.lower() == 'айди':
        bot.reply_to(message, f'ID: {message.from_user.id}')

bot.polling(none_stop=True)
