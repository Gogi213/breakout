# binance_api.py

import requests
import pandas as pd


def get_top_futures_pairs(base_currency='USDT', limit=3):
    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Error fetching data from Binance Futures API")

    data = response.json()
    pairs = [item for item in data if item['symbol'].endswith(base_currency)]
    pairs.sort(key=lambda x: float(x['quoteVolume']), reverse=True)
    return [pair['symbol'] for pair in pairs[:limit]]


def get_historical_futures_data(symbol, interval='15m', limit=500):
    url = f"https://fapi.binance.com/fapi/v1/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching data for {symbol}")

    data = response.json()
    df = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    return df
