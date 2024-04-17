import requests


def emoji(pre):
    if pre.startswith('-'):
        return f'{pre} 🔴'
    else:
        return f'{pre} 🟢'


def btc():
    url = requests.get(f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD')
    data = url.json()
    # high = data['RAW']['BTC']['USD']['HIGHDAY']
    # low = data['RAW']['BTC']['USD']['LOWDAY']
    pre = str(data['RAW']['BTC']['USD']['CHANGEPCT24HOUR'])[0:5] + '%'
    res = [data['RAW']['BTC']['USD']['PRICE'], emoji(pre)]
    print(high, low)
    return res


def eth():
    url = requests.get(f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=ETH&tsyms=USD')
    data = url.json()
    # high = data['RAW']['ETH']['USD']['HIGHDAY']
    # low = data['RAW']['ETH']['USD']['LOWDAY']
    pre = str(data['RAW']['ETH']['USD']['CHANGEPCT24HOUR'])[0:5] + '%'
    res = [data['RAW']['ETH']['USD']['PRICE'], emoji(pre)]
    return res


def ltc():
    url = requests.get(f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=LTC&tsyms=USD')
    data = url.json()
    # high = data['RAW']['LTC']['USD']['HIGHDAY']
    # low = data['RAW']['LTC']['USD']['LOWDAY']
    pre = str(data['RAW']['LTC']['USD']['CHANGEPCT24HOUR'])[0:5] + '%'
    res = [data['RAW']['LTC']['USD']['PRICE'], emoji(pre)]
    return res


def doge():
    url = requests.get(f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=DOGE&tsyms=USD')
    data = url.json()
    pre = str(data['RAW']['DOGE']['USD']['CHANGEPCT24HOUR'])[0:5] + '%'
    res = [data['RAW']['DOGE']['USD']['PRICE'], emoji(pre)]
    return res


def xrp():
    url = requests.get(f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=XRP&tsyms=USD')
    data = url.json()
    pre = str(data['RAW']['XRP']['USD']['CHANGEPCT24HOUR'])[0:5] + '%'
    res = [data['RAW']['XRP']['USD']['PRICE'], emoji(pre)]
    return res


def bnb():
    url = requests.get(f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BNB&tsyms=USD')
    data = url.json()
    pre = str(data['RAW']['BNB']['USD']['CHANGEPCT24HOUR'])[0:5] + '%'
    res = [data['RAW']['BNB']['USD']['PRICE'], emoji(pre)]
    return res


def crypto():
    price_btc = btc()
    price_eth = eth()
    price_ltc = ltc()
    price_xrp = xrp()
    price_bnb = bnb()
    price_doge = doge()
    result = (f'<b>BTC:</b>\n<code>{price_btc[0]}$</code>\n<code>{price_btc[1]}</code>\n\n'
              f'<b>ETH:</b>\n<code>{price_eth[0]}$</code>\n<code>{price_eth[1]}</code>\n\n'
              f'<b>LTC:</b>\n<code>{price_ltc[0]}$</code>\n<code>{price_ltc[1]}</code>\n\n'
              f'<b>XRP:</b>\n<code>{price_xrp[0]}$</code>\n<code>{price_xrp[1]}</code>\n\n'
              f'<b>DOGE:</b>\n<code>{price_doge[0]}$</code>\n<code>{price_doge[1]}</code>'
              f'<b>BNB:</b>\n<code>{price_bnb[0]}$</code>\n<code>{price_bnb[1]}</code>\n\n')
    return result