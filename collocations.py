from telegram import Bot 
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import time
import random

# Ваш токен, который вы получили от BotFather
TOKEN = '8043514095:AAHktuhNYjI-aLTMyfaVZEudC2jJBy6OoFM'

# Словарь с темами и коллокациями
collocations = {
    "nature": [
        "breathtaking scenery - захватывающий дух пейзаж",
        "lush greenery - пышная зелень",
        "dense forest - густой лес",
        "majestic mountains - величественные горы",
        "crystal-clear water - кристально чистая вода"
    ],
    "weather": [
        "heavy rain - сильный дождь",
        "clear sky - ясное небо",
        "strong winds - сильный ветер",
        "thick fog - густой туман",
        "scorching heat - жгучая жара"
    ]
}

# Хранилище для выбранных пользователем тем и уже отправленных коллокаций
user_data = {}

# Функция для отправки сообщения
def send_daily_message(context: CallbackContext):
    chat_id = context.job.context
    topic = user_data.get(chat_id, {}).get("topic", "nature")  # Тема по умолчанию — "природа"
    
    sent_collocations = user_data.get(chat_id, {}).get("sent", [])
    available_collocations = [c for c in collocations[topic] if c not in sent_collocations]

    if available_collocations:
        message = random.choice(available_collocations)
        context.bot.send_message(chat_id=chat_id, text=message)

        # Обновляем список уже отправленных коллокаций
        user_data[chat_id]["sent"].append(message)
    else:
        context.bot.send_message(chat_id=chat_id, text="No more collocations available for today.")

# Функция /start для приветствия пользователя
def start(update, context):
    update.message.reply_text(
        "Hi! Choose a topic by typing /set_topic_nature or /set_topic_weather. "
        "I will send you a collocation for the chosen topic!"
    )

# Функция для установки темы и отправки коллокации сразу после выбора
def set_topic_nature(update, context):
    chat_id = update.message.chat_id
    user_data[chat_id] = {"topic": "nature", "sent": []}
    update.message.reply_text("You have selected the topic: nature")

    # Отправляем случайную коллокацию сразу после выбора темы
    message = random.choice(collocations["nature"])
    user_data[chat_id]["sent"].append(message)  # Обновляем список отправленных коллокаций
    update.message.reply_text(f"Here is your collocation: {message}")

def set_topic_weather(update, context):
    chat_id = update.message.chat_id
    user_data[chat_id] = {"topic": "weather", "sent": []}
    update.message.reply_text("You have selected the topic: weather")

    # Отправляем случайную коллокацию сразу после выбора темы
    message = random.choice(collocations["weather"])
    user_data[chat_id]["sent"].append(message)  # Обновляем список отправленных коллокаций
    update.message.reply_text(f"Here is your collocation: {message}")

# Функция для установки ежедневных сообщений
def set_daily_message(update, context):
    chat_id = update.message.chat_id
    context.job_queue.run_daily(send_daily_message, time=time(9, 0), context=chat_id)
    update.message.reply_text("Daily messages have been set!")

# Основная функция для запуска бота
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Команды /start, /set_topic_nature и /set_topic_weather
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("set_topic_nature", set_topic_nature))
    dp.add_handler(CommandHandler("set_topic_weather", set_topic_weather))
    dp.add_handler(CommandHandler("set_daily_message", set_daily_message))

    # Запуск бота
    updater.start_polling()

    # Ожидание завершения
    updater.idle()

if __name__ == '__main__':
    main()
