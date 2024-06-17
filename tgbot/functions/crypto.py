import aiohttp
import asyncio

import logging

logger = logging.getLogger(__name__)


def emoji(pre):
    if pre.startswith('-'):
        return f'{pre} 🔴'
    else:
        return f'{pre} 🟢'


async def get_price_and_change(crypto_symbol):
    url = f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={crypto_symbol}&tsyms=USD'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                price = data['RAW'][crypto_symbol]['USD']['PRICE']
                change_pct = str(data['RAW'][crypto_symbol]['USD']['CHANGEPCT24HOUR'])[0:5] + '%'
                return price, emoji(change_pct)
    except (aiohttp.ClientError, KeyError, ValueError) as err:
        logger.error(f"Error fetching data for {crypto_symbol}: {err}")
        return None


async def crypto() -> str:
    """
    Get parse info about favorite indexes.
    :return:
    Index with % changes and emoji status.
    """
    tasks = [
        get_price_and_change('BTC'),
        get_price_and_change('ETH'),
        get_price_and_change('LTC'),
        get_price_and_change('XRP'),
        get_price_and_change('BNB'),
        get_price_and_change('DOGE')
    ]

    prices = await asyncio.gather(*tasks)
    symbols = ['BTC', 'ETH', 'LTC', 'XRP', 'BNB', 'DOGE']

    result = ""
    for symbol, price in zip(symbols, prices):
        if price[0] is not None:
            result += f'<b>{symbol}:</b>\n<code>{price[0]}$</code>\n<code>{price[1]}</code>\n\n'
        else:
            result += f'<b>{symbol}:</b>\n<code>Error fetching data</code>\n\n'

    return result


async def index_price(index):
    if len(index) == 0:
        return "🐒 Щоб отримати ціну на конретний індекс, мабуть треба його хочаб вказати)) 0 IQ"
    elif len(index) > 7:
        return f"🦧 Більше 7 букв. Не читатиму."
    else:
        index_info = await get_price_and_change(index)

        if index_info is None:
            return f"🦉 Вибач, або був вказаний некоректний індекс, або я не можу отримати інформацію про <b>{index}</b>."
        else:
            price = f"""<b>{index}:</b>\n<code>{index_info[0]}$</code>\n<code>{index_info[1]}</code>"""
            return price
