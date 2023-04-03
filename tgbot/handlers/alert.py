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


async def alert_check(bot: Bot):
    if requests.get(link_state, headers=head).json()['state']['alert']:
        for chat in chats_id:
            await bot.send_message(chat_id=chat,
                                   text='🚨 Увага!\n\n'
                                        'Повітряна тривога у м. Київ!')
    else:
        pass


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