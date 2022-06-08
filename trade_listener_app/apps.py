from threading import Thread

from django.apps import AppConfig
from django.conf import settings

from trade_listener_app.simple_websocket import DeribitWS

class TradeListenerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trade_listener_app'

    def ready(self):
        print(f"App Trade Listener Starting.")

        client_id = settings.CREDENTIALS["READ_ONLY_1"]["KEY"]
        client_secret = settings.CREDENTIALS["READ_ONLY_1"]["SECRET"]
        ws = DeribitWS(user_account="USER_ACCOUNT",
                       client_id=client_id,
                       client_secret=client_secret)

        new_thread = Thread(target=ws.subscribe_all_trades)
        new_thread.start()

        from trade_listener_app.parser import parse_trades
        settings.INCOMING_TRADE_SIGNAL.connect(parse_trades)

        print(f"Exchange connection established.")
        settings.WS_LISTENER = ws
