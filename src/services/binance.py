from binance import AsyncClient, BinanceSocketManager
from binance.streams import ReconnectingWebsocket
from websockets.exceptions import ConnectionClosed

from schemas.binance import Event, Response
from services.base import BaseService
from utils.metrics import calculate_rsi


class Binance(BaseService):
    def __init__(self):
        self.symbol = "BTCUSDT"
        self.interval = "1s"
        super().__init__()

    async def subscribe(self):
        connection = await self.connect()
        async with connection as socket:
            try:
                await self.process(socket)
            except ConnectionClosed:
                pass

    async def connect(self) -> ReconnectingWebsocket:
        client = await AsyncClient.create()
        manager = BinanceSocketManager(client)
        return manager.kline_socket(symbol=self.symbol, interval=self.interval)

    def parse(self, message) -> Event | None:
        event = Event(**message)
        return event if event.kline.closed else None

    async def process(self, socket: ReconnectingWebsocket):
        while True:
            message = await socket.recv()
            event = self.parse(message)
            if event is None:
                continue
            rsi = self.calculate_metrics(event.kline, calculate_rsi)
            await self.send(Response, event.kline, rsi=rsi)
