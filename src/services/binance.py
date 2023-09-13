from binance import AsyncClient, BinanceSocketManager
from binance.enums import KLINE_INTERVAL_1SECOND
from binance.streams import ReconnectingWebsocket
from websockets.exceptions import ConnectionClosed

from schemas.binance import Event, Response
from utils.metrics import calculate_rsi


class Binance:
    def __init__(self):
        self.symbol = "BTCUSDT"
        self.interval = KLINE_INTERVAL_1SECOND
        self.klines = []

    async def subscribe(self):
        socket = await self.connect()
        async with socket as subscription:
            try:
                await self.process(subscription)
            except ConnectionClosed:
                pass

    async def process(self, subscription: ReconnectingWebsocket):
        while True:
            message = await subscription.recv()
            event = Event(**message)
            self.klines.append(event.kline)
            rsi = calculate_rsi(self.klines)
            response = Response(kline=event.kline, rsi=rsi)
            print(response.model_dump_json())

    async def connect(self) -> ReconnectingWebsocket:
        client = await AsyncClient.create()
        manager = BinanceSocketManager(client)
        return manager.kline_socket(symbol=self.symbol, interval=self.interval)
