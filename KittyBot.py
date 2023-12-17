from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup, Bot
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

secret_token = os.getenv('TOKEN')
url_cat = os.getenv('URL_cat')
url_dog = os.getenv('URL_dog')

updater = Updater(token=secret_token)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_new_image():
    try:
        response = requests.get(url_cat).json()
    except Exception as error:
        print(error)
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(url_dog).json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, Синтетический Апельсин')


def wake_up(update, context):
    # В ответ на команду /start
    # будет отправлено сообщение 'Спасибо, что включили меня'
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)
    chat = update.effective_chat
    name = update.message.chat.first_name
    print(update)
    context.bot.send_message(chat_id=chat.id,
                             text=f'Кто просил включать меня, Сученька? {name} это ты что ли?', reply_markup=button)


def main():
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
