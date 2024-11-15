from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, Application
from datetime import time
import random
import pandas as pd
from pytz import timezone
import datetime

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Чтение данных из Excel
df = pd.read_excel("./Collocations_DB.xlsx")

# Преобразование данных из Excel в словарь
collocations = {}
for index, row in df.iterrows():
    topic = row['topic']
    phrase = row['phrase']
    
    if topic not in collocations:
        collocations[topic] = []
    
    collocations[topic].append(phrase)

# Хранилище для выбранных пользователем тем и отправленных коллокаций
user_data = {}

# Московский часовой пояс
moscow_timezone = timezone('Europe/Moscow')

#приветствие
async def start(update, context):
    await update.message.reply_text(
        "Привет! Я бот, который помогает в изучении устойчивых сочетаний английского языка. "
        "Используйте /send_collocation для получения случайной коллокации или /set_daily_message для её ежедневной отправки."
    )

# Функция для установки темы
async def set_topic(update, context):
    chat_id = update.message.chat_id
    topic = update.message.text.split('_')[-1].replace('and', '_').replace(' ', '_')  # Получаем тему из команды

    if topic not in collocations:
        await update.message.reply_text("This topic does not exist. Please choose another one.")
        return

    user_data[chat_id] = {"topic": topic, "sent": []}
    await update.message.reply_text(f"You have selected the topic: {topic}")

    # Отправляем случайную коллокацию сразу после выбора темы
    message = random.choice(collocations[topic])
    user_data[chat_id]["sent"].append(message)  # Обновляем список отправленных коллокаций
    await update.message.reply_text(f"Here is your collocation: {message}")

#рандомная коллокация
async def send_collocation_command(update, context):
    chat_id = update.message.chat_id
    # Выбор случайной коллокации из всего DataFrame
    random_collocation = df.sample(1)['phrase'].values[0]  # Выбираем случайное значение из столбца 'phrase'
    await context.bot.send_message(chat_id=chat_id, text=random_collocation)

# Функция для автоматической отправки коллокации
def send_daily_message(context: CallbackContext):
    chat_id = context.job.context
    topic = user_data.get(chat_id, {}).get("topic")
    last_sent = user_data.get(chat_id, {}).get("last_sent")

    if topic and (not last_sent or last_sent.date() < datetime.datetime.now(moscow_timezone).date()):
        send_collocation(chat_id, topic, context)

# Команда для установки автоматической отправки сообщений в 8:00
async def set_daily_message(update, context):
    chat_id = update.message.chat_id
    context.job_queue.run_daily(send_daily_message, time=time(5, 30), context=chat_id, timezone=moscow_timezone)
    await update.message.reply_text("Daily messages have been set for 16:30 Moscow time!")

# Основная функция для запуска бота
def main():
    dp = Application.builder().token(TOKEN).build()

    # Обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("set_topic_nature", set_topic))
    dp.add_handler(CommandHandler("set_topic_weather", set_topic))
    dp.add_handler(CommandHandler("set_topic_emotions", set_topic))
    dp.add_handler(CommandHandler("set_topic_health", set_topic))
    dp.add_handler(CommandHandler("set_topic_economics", set_topic))
    dp.add_handler(CommandHandler("set_topic_education", set_topic))
    dp.add_handler(CommandHandler("set_topic_art", set_topic))
    dp.add_handler(CommandHandler("set_topic_sport", set_topic))
    dp.add_handler(CommandHandler("set_topic_technologies", set_topic))
    dp.add_handler(CommandHandler("set_topic_politics", set_topic))
    dp.add_handler(CommandHandler("set_topic_dialogue", set_topic))
    dp.add_handler(CommandHandler("set_topic_time", set_topic))
    dp.add_handler(CommandHandler("set_topic_law", set_topic))
    dp.add_handler(CommandHandler("set_topic_fashion", set_topic))
    dp.add_handler(CommandHandler("set_topic_shopping", set_topic))
    dp.add_handler(CommandHandler("set_topic_characteristics", set_topic))
    dp.add_handler(CommandHandler("set_topic_news", set_topic))
    dp.add_handler(CommandHandler("set_topic_idioms", set_topic))
    dp.add_handler(CommandHandler("send_collocation", send_collocation_command))
    # dp.add_handler(CommandHandler("set_daily_message", set_daily_message))

    dp.run_polling()

if __name__ == '__main__':
    main()
