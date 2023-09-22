from aiogram import Bot
from tgbot.config import load_config

import requests
from bs4 import BeautifulSoup

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
    pass


def get_latest_post_url():
    """
    Find in url list needed post by title.
    """
    base_urls = ['http://ukrpohliad.org/news', 'http://ukrpohliad.org/news/page/2']
    for base_url in base_urls:
        try:
            response = requests.get(base_url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')

            for article in soup.find_all('article'):
                target = article.find('div', class_='thumb-area')
                if target:
                    title_tag = target.find('a')
                    if title_tag and title_tag['title'].startswith('Загальні бойові втрати противника'):
                        return title_tag['href']

        except requests.RequestException as err:
            return f'An error occurred while processing the request:\n\n<code>{err}</code>'
        except Exception as err:
            return f'Нажаль, сталася помилка при обробці запиту бойових втрат:\n\n<code>{err}</code>'

    return "Статистика не була знайдена на етапі пошуку. Сценарій потребує доробки."


def get_image_stat(today_post):
    """Find and get feature jpg in selected post by link."""
    try:
        response = requests.get(today_post)
        response.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if tag.get('property', '') == 'og:image':
                return tag.get('content', '')

        return "Статистика бойових втрат не була отримана на етапі обробки. Сценарій потребує доробки."

    except requests.RequestException as err:
        return f'Під час обробки запиту виникла помилка:\n\n<code>{err}</code>'
    except Exception as err:
        return f'An unexpected error occurred:\n\n<code>{err}</code>'


async def daily_weather(bot: Bot):
    for chat in chats_id:
        await bot.send_message(chat_id=chat, text=get_weather_data())


async def daily_statistic(bot: Bot):
    img = get_image_stat(get_latest_post_url())
    for chat in chats_id:
        try:
            await bot.send_photo(chat_id=chat, photo=img)
        except Exception as err:
            await bot.send_message(chat_id=chat, text=img)