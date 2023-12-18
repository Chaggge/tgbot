from flask import Flask, request
import telebot
import os

app = Flask(__name__)

# Установите токен вашего бота

# Создайте экземпляр бота
bot = telebot.TeleBot(TOKEN_TG)

# Установите URL для вебхука
WEBHOOK_URL = 'https://echotg.onrender.com/' + TOKEN_TG

# Установите вебхук
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Hello! I am your bot.")

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
