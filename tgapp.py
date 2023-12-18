from flask import Flask, request
import telebot
import os
import requests
from telebot import types

TOKEN_TG = os.environ.get("TOKEN_TG")
WEATHERSTACK_API_KEY = os.environ.get('WEATHERSTACK_API_KEY')

app = Flask(__name__)

# Установите токен вашего бота

# Создайте экземпляр бота
bot = telebot.TeleBot(TOKEN_TG)

# Установите URL для вебхука
WEBHOOK_URL = 'https://echotg.onrender.com/' + TOKEN_TG


# Установите вебхук
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

def get_weather():
    # Формируем URL для запроса погоды в Новосибирске
    weatherstack_url = f'http://api.weatherstack.com/current?access_key={WEATHERSTACK_API_KEY}&query=Novosibirsk'
    
    # Отправляем GET-запрос к API
    response = requests.get(weatherstack_url)
    
    # Проверяем успешность запроса
    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temperature']
        description = data['current']['weather_descriptions'][0]
        return f'Текущая температура в Новосибирске: {temperature}°C\n{description}'
    else:
        return 'Не удалось получить информацию о погоде'

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("/weather")
    markup.add(item1)
    bot.reply_to(message, "Привет я - эхо бот и не только?", reply_markup=markup)

@bot.message_handler(commands=['weather'])
def handle_weather(message):
    weather_info = get_weather()
    bot.send_message(message.chat.id, weather_info)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, message.text)

# Подключение вебхука к Flask
@app.route('/' + TOKEN_TG, methods=['GET','POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return '', 200

if __name__ == '__main__':
    # Запуск Flask-приложения
    app.run(port=int(os.environ.get('PORT', 5000)), host='0.0.0.0')
