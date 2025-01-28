import requests
from  keys import *
import json

def get_old_prices(sym):
    url = f"https://data.alpaca.markets/v2/stocks/{sym}/bars?timeframe=1T&feed=iex"
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": KEY[0],
        "APCA-API-SECRET-KEY": KEY[1]
    }

    response = requests.get(url, headers=headers)
    bars = json.loads(response.text)['bars']
    return [bar['vw'] for bar in bars]

def get_price(sym):
    url = f'https://data.alpaca.markets/v2/stocks/{sym}/bars/latest'
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": KEY[0],
        "APCA-API-SECRET-KEY": KEY[1]
    }
    
    response = requests.get(url, headers=headers)
    return json.loads(response.text)['bar']['vw']

def syminfo(sym):
    url = f'https://{ENDP}api.alpaca.markets/v2/assets/{sym}'
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": KEY[0],
        "APCA-API-SECRET-KEY": KEY[1]
    }
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

def buy(sym, amnt):
    url = f'https://{ENDP}api.alpaca.markets/v2/orders'
    
    payload = {
        "type": "market",
        "time_in_force": "day",
        "side": 'buy',
        "symbol": sym,
        "notional": amnt,
    }
    
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": KEY[0],
        "APCA-API-SECRET-KEY": KEY[1]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return json.loads(response.text)

def sell(sym):
    url = f'https://{ENDP}api.alpaca.markets/v2/orders'
    
    payload = {
        "type": "market",
        "time_in_force": "day",
        "side": 'sell',
        "symbol": sym,
        "notional": get_all_amnt(sym),
    }
    
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": KEY[0],
        "APCA-API-SECRET-KEY": KEY[1]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return json.loads(response.text)

def get_all_amnt(sym):
    url = f"https://{ENDP}api.alpaca.markets/v2/positions/{sym}"

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": KEY[0],
        "APCA-API-SECRET-KEY": KEY[1]
    }
    
    response = requests.get(url, headers=headers)
    return json.loads(response.text)['qty_avaliable']

def get_clock():
    url = f'https://{ENDP}api.alpaca.markets/v2/clock'
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": KEY[0],
        "APCA-API-SECRET-KEY": KEY[1]
    }
    
    response = requests.get(url, headers=headers)
    return json.loads(response.text)