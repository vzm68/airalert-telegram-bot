from aiogram import Bot
from tgbot.config import load_config

import requests
from bs4 import BeautifulSoup

chats_id = load_config(".env").tg_bot.chats

url = 'https://ua.sinoptik.ua/погода-київ'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')  # Parse sinoptik.ua page as html
block_days = soup.find('div', {'id': 'blockDays'})  # Get info block by ID what I need
bd1 = block_days.find('div', {'id': 'bd1'})  # Get today info block about data and temperature
weather_ico = soup.find('div', {'class': 'weatherIco'})
description = soup.find('div', {'class': 'wDescription clearfix'}).text.strip()
infoDaylight = soup.find('div', {'class': 'infoDaylight'}).text

today_data = " ".join(bd1.text.split()[:3])  # Example: Понеділок 03 квітня
today_weather = " ".join(bd1.text.split()[3:])  # Example: мін. +4° макс. +8°
title = weather_ico['title']  # Example: Хмарно, дощ
sunrise = infoDaylight.split()[1]
sunset = infoDaylight.split()[3]


async def daily_news(bot: Bot):
    for chat in chats_id:
        await bot.send_message(chat_id=chat, text=f'🗓{today_data}\n\n'
                                                  f'🔆 Погода у Києві\n'
                                                  f'{today_weather} ({title})\n\n'
                                                  f'{description}\n\n'
                                                  f'Схід: {sunrise} 🌤\n'
                                                  f'Захід: {sunset} 🌒')
