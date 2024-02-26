from aiogram import Bot
from tgbot.config import load_config

import requests
from bs4 import BeautifulSoup
import feedparser

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


def get_daily_news():
    rss_url = "https://rss.unian.net/site/news_ukr.rss"

    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Extract titles and links for the last 3 entries
    latest_entries = feed.entries[:3]
    titles_and_links = [(entry.title, entry.link) for entry in latest_entries]

    result_string = ""

    # Print the last 3 titles and links
    for title, link in titles_and_links:
        result_string += f'{title}\n<a href="{link}">Посилання</a>\n\n'

    return result_string


def get_image_stat():
    # RSS feed to parse
    rss_url = 'https://ukrpohliad.org/feed'

    # Make a request to the RSS feed
    response = requests.get(rss_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the XML content of the RSS feed
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('item')
        for item in items:
            if str(item.title.text).startswith('Загальні бойові втрати противника'):
                content = item.find_next('content:encoded').text
                content_soup = BeautifulSoup(content, 'html.parser')
                img_link = content_soup.find('img')['src']
                return img_link

    else:
        return f'Не вдалося отримати RSS-стрічку. Status code: {response.status_code}'


async def daily_weather(bot: Bot):
    for chat in chats_id:
        await bot.send_message(chat_id=chat, text=get_weather_data())


async def daily_statistic(bot: Bot):
    img = get_image_stat()
    for chat in chats_id:
        try:
            await bot.send_photo(chat_id=chat, photo=img)
        except Exception as err:
            await bot.send_message(chat_id=chat, text=img)


async def daily_news(bot: Bot):
    news = get_daily_news()
    for chat in chats_id:
        try:
            await bot.send_message(chat_id=chat, text=news)
        except Exception as err:
            await bot.send_message(chat_id=chat, text=f"<code>{err}</code>")