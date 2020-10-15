import alpaca_trade_api as tradeapi
import keys

api_key = keys.api_key
api_secret = keys.api_secret
base_url = keys.base_url

# instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# obtain account information
account = api.get_account()
print(account)

APCA_API_KEY_ID = api_key
APCA_API_SECRET_KEY = api_secret
APCA_API_BASE_URL = base_url

api = tradeapi.REST(key_id=api_key, secret_key=api_secret, base_url=base_url, api_version='v2')

barset = api.get_barset('AAPL', 'day', limit=5)

aapl_bars = barset['AAPL']
# See how much AAPL moved in that timeframe.
week_open = aapl_bars[0].o
week_close = aapl_bars[-1].c
percent_change = (week_close - week_open) / week_open * 100
print('AAPL moved {}% over the last {} days'.format(percent_change, 5))
