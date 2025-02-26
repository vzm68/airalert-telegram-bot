from aiogram import Bot
from tgbot.config import load_config
from tgbot.functions.crypto import crypto
from tgbot.functions.tuya_devices import tuya_sensors_info

import requests
from bs4 import BeautifulSoup
import feedparser

chats_id = load_config(".env").tg_bot.chats


def get_weather_data():
    """
    Parse sinoptik.ua page for class elements.
    Info about day and weather reaches through a.vV3dvPLZ.uXujd8Ct element.

    :param url: str - URL страницы с прогнозом погоды
    :return: str - текст с прогнозом погоды
    """
    url = "https://sinoptik.ua/pohoda/kyiv"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"❌ Network error: {e}"

    soup = BeautifulSoup(response.text, "html.parser")

    weather_block = soup.select_one("a.vV3dvPLZ.uXujd8Ct")
    if not weather_block:
        return "❌ Can't reach weather block."

    data_day = weather_block.select_one("p.BzO81ZRx")
    data_number = weather_block.select_one("p.BrJ0wZrO")
    data_month = weather_block.select_one("p:nth-of-type(3)")

    data_day = data_day.get_text(strip=True) if data_day else "Fetch failed"
    data_number = data_number.get_text(strip=True) if data_number else "Fetch failed"
    data_month = data_month.get_text(strip=True) if data_month else "Fetch failed"

    temp_blocks = weather_block.select("div.cFBF0wTW")
    data_min = temp_blocks[0].get_text(strip=True) if len(temp_blocks) > 0 else "Fetch failed"
    data_max = temp_blocks[1].get_text(strip=True) if len(temp_blocks) > 1 else "Fetch failed"

    status_element = weather_block.select_one("div.EAadAKAr")
    data_status = status_element.get("aria-label", "Невідомо") if status_element else "Fetch failed"

    description_element = soup.select_one("div.kQfVVnhb div.ozYkFc9V p.DGqLtBkd")
    description = description_element.get_text(strip=True) if description_element else "Description failed"

    sunriset_element = soup.select_one("div.STD2Z4-t p._58CF6Vul.Q-AjjW65.J93b4WdE")
    sunriset = sunriset_element.get_text().split() if sunriset_element else []

    sunrise = sunriset[1] if len(sunriset) > 1 else "Fetch failed"
    sunset = sunriset[3] if len(sunriset) > 3 else "Fetch failed"

    return (
        f"🗓 {data_day.title()} {data_number} {data_month}\n\n"
        f"🔆 Погода у Києві\n"
        f"{data_min} {data_max} ({data_status})\n\n"
        f"{description}\n\n"
        f"Схід: 🌤 {sunrise}\n"
        f"Захід: 🌒 {sunset}"
    )


def get_daily_news():
    rss_url = "https://rss.unian.net/site/news_ukr.rss"

    feed = feedparser.parse(rss_url)
    latest_entries = feed.entries[:3]

    return "\n\n".join(
        f'{entry.title}\n<a href="{entry.link}">Посилання</a>'
        for entry in latest_entries
    )


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


async def daily_crypto(bot: Bot):
    for chat in chats_id:
        try:
            price = await crypto()
            await bot.send_message(chat_id=chat, text=price)
        except Exception as err:
            await bot.send_message(chat_id=chat, text=f"<code>{err}</code>")


async def daily_tuya(bot: Bot):
    for chat in chats_id:
        try:
            await bot.send_message(chat_id=chat, text=tuya_sensors_info())
        except Exception as err:
            await bot.send_message(chat_id=chat, text=f"<code>{err}</code>")


async def weekly_donat(bot: Bot):
    for chat in chats_id:
        await bot.send_message(chat_id=chat, text="Ви можете підтримати розробку та обслуговування бота!\n"
                                                  "Долучайтесь на Патреон за посиланням: https://patreon.com/6x8\n"
                                                  "Або донат на банку: https://send.monobank.ua/jar/5QiFnjCPYq\n",
                               disable_web_page_preview=True)