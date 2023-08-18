from aiogram import Bot
from tgbot.config import load_config

import requests
from bs4 import BeautifulSoup
import re

chats_id = load_config(".env").tg_bot.chats


def get_weather_data():
    weather_url = 'https://ua.sinoptik.ua/погода-київ'
    try:
        response = requests.get(weather_url)
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

        return f'🗓{today_data}\n\n' \
               f'🔆 Погода у Києві\n' \
               f'{today_weather} ({title})\n\n' \
               f'{description}\n\n' \
               f'Схід: {sunrise} 🌤\n' \
               f'Захід: {sunset} 🌒'
    except Exception as err:
        return f"Нажаль, сталася помилка...🦦\n\n" \
               f"Інформація не була отримана: <code>{err}</code>."


def get_war_statistic():
    url = "https://index.minfin.com.ua/ua/russian-invading/casualties/"
    try:
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'html.parser')
        result = soup.find('div', {'class': 'casualties'})
        text = result.text.strip()
        pattern = r"[\d]+(?:\s?\(\D\d+\))?"
        result = re.findall(pattern, text)
        return f"📠 Орієнтовні втрати противника:\n" \
               f"☠ <b>Особовий склад:</b> {result[12]} (<b>+{result[13]}</b>)\n" \
               f"▪ Танки: {result[0]}\n" \
               f"▪ ББМ: {result[1]}\n" \
               f"▪ Гармати: {result[2]}\n" \
               f"▪ РСЗВ: {result[3]}\n" \
               f"▪ Засоби ППО: {result[4]}\n" \
               f"🛩 Літаки: {result[5]}\n" \
               f"🚁 Гелікоптери: {result[6]}\n" \
               f"🛸 БПЛА: {result[7]}\n" \
               f"🚀 Крилаті ракети: {result[8]}\n" \
               f"🚤 Кораблі (катери): {result[9]}\n" \
               f"🚛 Автомобілі та автоцистерни: {result[10]}\n" \
               f"🚚 Спеціальна техніка: {result[11]}\n"
    except Exception as err:
        return f"Нажаль, сталася помилка...🦦\n\n" \
               f"Інформація не була отримана: <code>{err}</code>."


def get_daily_news():
    pass


async def daily_weather(bot: Bot):
    for chat in chats_id:
        await bot.send_message(chat_id=chat, text=get_weather_data())


async def daily_statistic(bot: Bot):
    for chat in chats_id:
        await bot.send_message(chat_id=chat, text=get_war_statistic())