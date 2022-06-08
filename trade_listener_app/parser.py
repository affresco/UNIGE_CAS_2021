import random
from django.conf import settings

from trade_listener_app.models import TradeData


def parse_trades(sender, trades):
    print(f"{trades}")

    output = []

    # Randomly attribute trades to a given user (for the deo)
    user_id = 0 if random.random() < 0.5 else 1

    for trade in trades:

        try:
            hash_ = TradeData.compute_hash(
                user_id=user_id,
                trade_seq=trade["trade_seq"],
                timestamp=trade["timestamp"],
                price=trade["price"],
                quantity=trade["amount"],
                direction=trade["direction"],
                instrument_name=trade["instrument_name"],
            )

            t = TradeData(
                user_id=user_id,
                trade_seq=trade["trade_seq"],
                trade_id=trade["trade_id"],
                timestamp=trade["timestamp"],
                price=trade["price"],
                currency=trade["instrument_name"].split("-")[1],
                instrument_name=trade["instrument_name"],
                index_price=trade["index_price"],
                direction=1 if "buy" in trade["direction"] else -1,
                quantity=trade["amount"],
                hash=hash_[0:256]  # limit length to 256 chars
            )
            output.append(t)

        except Exception as exc:
            print(exc)

        # Create in database
        for t in output:
            if t.user_id not in settings.TRADE_DB_OBJECTS_BUFFER:
                settings.TRADE_DB_OBJECTS_BUFFER[t.user_id] = []

            settings.TRADE_DB_OBJECTS_BUFFER[t.user_id].append(t)


"""
'trade_seq': 74061137
'trade_id': '108165215'
'timestamp': 1654536184117
'tick_direction': 0
'price': 31127.0
'mark_price': 31120.61
'instrument_name': 'BTC-PERPETUAL'
'index_price': 31120.51
'direction': 'sell'
'amount': 1200.0
"""

# [{'trade_seq': 11032834, 'trade_id': 'ETH-13729753', 'timestamp': 1654536332998, 'tick_direction': 2, 'price': 1852.22, 'mark_price': 1852.2, 'instrument_name': 'ETH-PERPETUAL', 'index_price': 1851.43, 'direction': 'buy', 'combo_id': 'ETH-FS-17JUN22_PERP', 'block_trade_id': 'ETH-98323', 'amount': 50470.0}]
