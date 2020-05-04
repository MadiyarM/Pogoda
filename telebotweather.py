import telebot
import pyowm
import os

from telebot import types

owm = pyowm.OWM('5e3f9c18f57d1695f67c9726d7ed3d49', language="ru")
bot = telebot.TeleBot("881811359:AAHCa1oZ6YlnP3DEbYprnV442qCjP2y_o80")

@bot.message_handler(commands=['start'])
def welcome(message):

    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Готов мне помочь?')

    markup.add(item1)
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\n Я - {1.first_name}, бот созданный для советов !".format(message.from_user, bot.get_me()),  reply_markup=markup)


@bot.message_handler(content_types=['text'])
def markup(message):
    if message.chat.type == 'private':
        if message.text == 'Готов мне помочь?':
            bot.send_message(message.chat.id, 'Да, всегда готов!')
        else:
            send_advice(message)
	#bot.reply_to(message, message.text)
    #bot.send_message(message.chat.id, message.text)
    
@bot.message_handler(content_types=['text'])
def send_advice(message):
    observation = owm.weather_at_place(message.text)
    w = observation.get_weather()
    temp = w.get_temperature('celsius')['temp']

    answer = "В городе " + message.text + " сейчас " + w.get_detailed_status() + "\n"
    answer += "Температура равна " + str(temp) + "\n\n"
    if temp < 10:
        answer +='В городе ' + message.text + " оденьтесь теплее"

    elif temp < 20:
        answer +='Погода шикарная! Город ' + message.text + ' Вам очень рад!'

    elif temp > 20:
        answer +='Очень жарко!'

    bot.send_message(message.chat.id,  answer)

bot.polling()