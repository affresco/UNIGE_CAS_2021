import asyncio
import websockets
import json
from django.conf import settings

from blinker import Signal

trade_event = Signal("Incoming-Trade")


class DeribitWS:

    def __init__(self, user_account, client_id, client_secret):

        # A sub-account for a given user
        self.user_account = user_account
        # settings.TRADE_BUFFER[self.user_account] = []

        self.client_id = client_id
        self.client_secret = client_secret
        self.url = 'wss://test.deribit.com/ws/api/v2'

        self.auth_creds = {
            "jsonrpc": "2.0",
            "id": 0,
            "method": "public/auth",
            "params": {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        }
        self.test_creds()

    async def pub_api(self, msg):
        async with websockets.connect(self.url) as websocket:
            print(msg)
            await websocket.send(msg)
            while websocket.open:
                response = await websocket.recv()
                return json.loads(response)

    async def pub_api_2(self, msg):

        async with websockets.connect(self.url) as websocket:
            await websocket.send(msg)
            while websocket.open:

                response = await websocket.recv()

                # Parse
                json_response = json.loads(response)

                try:
                    # Extract trade info
                    trades = json_response["params"]["data"]

                    # Notify the system that new trades have arrived
                    settings.INCOMING_TRADE_SIGNAL.send(self.user_account, trades=trades)

                except Exception as exc:
                    print(exc)


    async def priv_api(self, msg):
        async with websockets.connect(self.url) as websocket:
            await websocket.send(json.dumps(self.auth_creds))
            while websocket.open:
                response = await websocket.recv()
                await websocket.send(msg)
                response = await websocket.recv()
                break
            return json.loads(response)

    @staticmethod
    def async_loop(api, message):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return asyncio.get_event_loop().run_until_complete(api(message))

    def test_creds(self):
        response = self.async_loop(self.pub_api, json.dumps(self.auth_creds))
        if 'error' in response.keys():
            raise Exception(f"Auth failed with error {response['error']}")
        else:
            print("Auth creds are good, it worked")

    def subscribe_all_trades(self):
        msg = {"jsonrpc": "2.0",
               "method": "public/subscribe",
               "id": 42,
               "params": {
                   "channels": ["trades.BTC-PERPETUAL.100ms",
                                "trades.ETH-PERPETUAL.100ms",
                                "trades.SOL-PERPETUAL.100ms",]}
               }
        response = self.async_loop(self.pub_api_2, json.dumps(msg))

