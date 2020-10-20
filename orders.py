import requests, json
from config import *

account_url = f"{base_url}/v2/account"
orders_url = f"{base_url}/v2/orders"
headers = {'APCA-API-KEY-ID': api_key, 'APCA-API-SECRET-KEY': api_secret}


def get_account():
    r = requests.get(account_url, headers=headers)

    return json.loads(r.content)


def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }

    r = requests.post(orders_url, json=data, headers=headers)

    return json.loads(r.content)

