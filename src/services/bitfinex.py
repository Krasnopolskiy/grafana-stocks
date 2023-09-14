from aiohttp import ClientSession, ClientWebSocketResponse, WSMessage, WSMsgType

from schemas.bitfinex import Event, Handshake, Response
from services.base import BaseService
from utils.metrics import calculate_vwap


class Bitfinex(BaseService):
    def __init__(self):
        self.url = "wss://api-pub.bitfinex.com/ws/2"
        self.symbol = "tBTCUSD"
        self.interval = "1m"
        super().__init__()

    def parse(self, message: WSMessage) -> Event | None:
        if message.type != WSMsgType.TEXT:
            return None
        try:
            data = message.json()
            return Event(*data)
        except TypeError:
            return None

    async def process(self, socket: ClientWebSocketResponse):
        async for message in socket:
            event = self.parse(message)
            if event is None:
                continue
            vwap = self.calculate_metrics(event.kline, calculate_vwap)
            await self.send(Response, event.kline, vwap=vwap)

    async def connect(self, socket: ClientWebSocketResponse):
        key = f"trade:{self.interval}:{self.symbol}"
        handshake = Handshake(key=key)
        await socket.send_str(handshake.model_dump_json())

    async def subscribe(self):
        async with ClientSession().ws_connect(self.url) as socket:
            await self.connect(socket)
            await self.process(socket)
