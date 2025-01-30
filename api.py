import requests
from colorama import Fore
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
    try:
        return [bar['vw'] for bar in bars]
    except:
        return 'no data'

def get_price(sym):
    url = f'https://data.alpaca.markets/v2/stocks/{sym}/bars/latest'
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": KEY[0],
        "APCA-API-SECRET-KEY": KEY[1]
    }
    
    response = requests.get(url, headers=headers)
    return json.loads(response.text)['bar']['c']

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
    
    print(Fore.GREEN + sym + Fore.RESET, end=' ')
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return json.loads(response.text)

def sell(sym, bought_price):
    url = f'https://{ENDP}api.alpaca.markets/v2/orders'
    
    payload = {
        "type": "market",
        "time_in_force": "day",
        "side": 'sell',
        "symbol": sym,
        "notional": get4rel(bought_price, sym),
    }
    
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": KEY[0],
        "APCA-API-SECRET-KEY": KEY[1]
    }
    
    print(Fore.RED + sym + Fore.RESET, end=' ')
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
    return json.loads(response.text)['qty_available']

def get_clock():
    url = f'https://{ENDP}api.alpaca.markets/v2/clock'
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": KEY[0],
        "APCA-API-SECRET-KEY": KEY[1]
    }
    
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

def oneminleft(clock):
    now = clock['timestamp'].split('T')[1].split(':')[:2]
    close = clock['next_close'].split('T')[1].split(':')[:2]
    if now[0] == close[0] and int(close[1]) - int(now[1]) == 1:
        return True
    
def get_cash():
    url = f'https://{ENDP}api.alpaca.markets/v2/account'
    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": KEY[0],
        "APCA-API-SECRET-KEY": KEY[1]
    }
    
    response = requests.get(url, headers=headers)
    return json.loads(response.text)['equity']

def get4rel(amnt, sym):
    p = get_price(sym)
    return amnt / p * 4