from aiogram import Dispatcher
from aiogram.types import Message
from tgbot.config import load_config


import requests

api_alert = load_config(".env").tg_bot.api_alert  # Get API alert from .env


link_state = "https://alerts.com.ua/api/states/25"  # I choose a specific region in my case
history = "https://alerts.com.ua/api/history/"  # History of alerts
head = {'X-API-Key': api_alert}  # Header to request


async def alert_check(dp: Dispatcher):
    if requests.get(link_state, headers=head).json()['state']['alert']:
        await dp.bot.send_message(chat_id=274309731, text='True')
    else:
        await dp.bot.send_message(chat_id=274309731, text='No alert!')


def register_alert(dp: Dispatcher):
    dp.register_message_handler(alert_check, commands=['test'])