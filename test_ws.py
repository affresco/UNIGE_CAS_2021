import json
import time

from api_clients.delta.unified.subscription import SubscriptionClient
from api_clients.delta.unified.requests import RequestClient
from trade_listener_app.incoming import on_incoming


def print_this(*args, **kwargs):
    print(args)
    print(kwargs)


f = open("./creds.json")
data = json.load(f)

read_only = data["READ_ONLY_1"]

ws = SubscriptionClient(
    url=read_only["URL"],
    key=read_only["KEY"],
    secret=read_only["SECRET"],
    callback=print_this,
)


ws.subscribe_to_all_trades(callback=print_this)

client = RequestClient(
    url=read_only["URL"],
    key=read_only["KEY"],
    secret=read_only["SECRET"],
)

client.account_summary(currency="BTC",)

while True:
    time.sleep(1.0)
    print("listening...")
    client.buy(instrument="BTC-PERPETUAL", amount=10.0)
