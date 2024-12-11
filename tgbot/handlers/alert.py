from datetime import datetime

from aiogram import Dispatcher, Bot
from aiogram.types import Message
from tgbot.config import load_config
from tgbot.functions.pinger import check_ips

import requests

api_alert = load_config(".env").tg_bot.api_alert  # Get API alert from .env
chats_id = load_config(".env").tg_bot.chats
admins = load_config(".env").tg_bot.admin_ids

link_state = f"https://api.alerts.in.ua/v1/iot/active_air_raid_alerts/31.json?token={api_alert}"


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
    global flag  # Not a good idea to use global var, but it's solution in my case. Func must be changed to class (!)
    global time
    try:
        status = requests.get(link_state).json()  # A means Alert N means clear and P particular alert
        if status == "A" and flag is False:
            time = datetime.now().strftime('%Y-%m-%d %H:%M')  # Save fixed time data to our global var
            flag = True
            for chat in chats_id:
                await bot.send_message(chat_id=chat,
                                       text='🚨 Увага!\n\n'
                                            'Повітряна тривога у м. Київ!')
        elif flag is True and status == "N":
            flag = False
            for chat in chats_id:
                await bot.send_message(chat_id=chat, text=f'{stop_alert(time)}')
    except Exception as err:
        for admin in admins:
            await bot.send_message(chat_id=admin, text=f"Exception during execute alert_check func:\n\n{err}")


async def get_map(message: Message):
    await message.reply(
        text='Мапа тривог тимчасово доступна за <a href="https://alerts.in.ua/lite">посиланням</a>.',
        disable_web_page_preview=False
    )


async def ping(bot: Bot):
    try:
        changes = await check_ips()
        for name, change in changes.items():
            if change['duration'] is not None:
                for chat in chats_id:
                    await bot.send_message(chat_id=chat,
                                           text=f"🌐 <b>{name}</b> {change['status']} {change['duration']}")
            else:
                for chat in chats_id:
                    await bot.send_message(chat_id=chat,
                                           text=f"🌐 <b>{name}</b> {change['status']}")
    except Exception as err:
        for admin in admins:
            await bot.send_message(chat_id=admin, text=f"Exception during execute ping func:\n\n{err}")


def register_alert(dp: Dispatcher):
    dp.register_message_handler(get_map, commands=['map'])
