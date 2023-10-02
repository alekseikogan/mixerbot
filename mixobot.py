import os
import requests

from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup
from dotenv import load_dotenv


load_dotenv()
secret_token = os.getenv('TOKEN')

updater = Updater(token=secret_token)
URL = {
    'ip': 'https://api.ipify.org?format=json',
    'cat': 'https://api.thecatapi.com/v1/images/search'}


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Ты заебал писать!!!11')


def get_ip():
    """Выдает твой ip"""
    response = requests.get(URL['ip']).json()
    your_ip = response.get('ip')
    return f' Твой ip:\n{your_ip}'


def new_ip(update, context):
    """Отправляет сообщение с ip"""
    chat = update.effective_chat
    context.bot.send_message(chat.id, get_ip())


def get_new_image():
    """Формирует изображение котика"""
    response = requests.get(URL['cat']).json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    """Отправляет сообщение с котиком"""
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def wake_up(update, context):
    """Действия после начала работы"""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([
        ['/get_ip', '/newcat']
        ],
        resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Я ПРОСНУЛСЯ!!!11',
        reply_markup=button)

    context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}.\n Вот твой ip: {get_ip()}',
        reply_markup=button)

    context.bot.send_message(
        chat_id=chat.id,
        text='... и ваш котик ...',
        reply_markup=button)

    context.bot.send_photo(chat.id, get_new_image())


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
updater.dispatcher.add_handler(CommandHandler('get_ip', new_ip))
updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

updater.start_polling()
updater.idle()
