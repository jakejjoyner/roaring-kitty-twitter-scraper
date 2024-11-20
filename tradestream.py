import config
from alpaca.trading.stream import TradingStream

trade_stream_client = TradingStream(api_key=config.api_key, secret_key=config.api_secret)

async def trade_updates_handler(data):
    print(data)

trade_stream_client.subscribe_trade_updates(trade_updates_handler)
trade_stream_client.run()

