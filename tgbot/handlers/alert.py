from datetime import datetime

from aiogram import Dispatcher, Bot
from aiogram.types import Message
from tgbot.config import load_config

import requests

api_alert = load_config(".env").tg_bot.api_alert  # Get API alert from .env
chats_id = load_config(".env").tg_bot.chats

link_state = "https://alerts.com.ua/api/states/25"  # I choose a specific region in my case
history_link = "https://alerts.com.ua/api/history"  # History of alerts
map_link = "https://alerts.com.ua/map.png"  # Map content
head = {'X-API-Key': api_alert}  # Header to request


def stop_alert(date):
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M')
    date1 = datetime.strptime(date, '%Y-%m-%d %H:%M')
    date2 = datetime.strptime(date_now, '%Y-%m-%d %H:%M')
    delta = date2 - date1
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    if days > 0:
        return f"❎ Відбій тривоги!\n" \
               f"Тривалість: <b>{days}</b> д., <b>{hours}</b> год., <b>{minutes}</b> хв. ⏱"
    elif hours > 0:
        return f"❎ Відбій тривоги!\n" \
               f"Тривалість: <b>{hours}</b> год., <b>{minutes}</b> хв. ⏱"
    else:
        return f"❎ Відбій тривоги!\n" \
               f"Тривалість: <b>{minutes}</b> хв. ⏱"


flag = False
time = ''


async def alert_check(bot: Bot):
    global flag  # Not a good idea to use global var, but it's solution in my case
    global time

    status = requests.get(link_state, headers=head).json()['state']['alert']  # Get True/False
    if status is True and flag is False:
        time = datetime.now().strftime('%Y-%m-%d %H:%M')  # Save fixed time data to our global var
        flag = True
        for chat in chats_id:
            await bot.send_message(chat_id=chat,
                                   text='🚨 Увага!\n\n'
                                        'Повітряна тривога у м. Київ!')
    elif flag is True and status is False:
        flag = False
        for chat in chats_id:
            await bot.send_message(chat_id=chat, text=f'{stop_alert(time)}')


async def get_map(message: Message):
    await message.reply_photo(requests.get(map_link).content)


async def get_history(message: Message):
    """
    Temporary don't use. This for future
    :param message:
    :return:
    """
    history = requests.get(history_link, headers=head).text
    await message.reply(text=history)


def register_alert(dp: Dispatcher):
    dp.register_message_handler(get_map, commands=['map'])
