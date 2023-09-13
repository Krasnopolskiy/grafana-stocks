from aiohttp import ClientSession, ClientWebSocketResponse, WSMessage, WSMsgType

from schemas.bitfinex import Event, Handshake, Response
from utils.metrics import calculate_vwap


class Bitfinex:
    def __init__(self):
        self.url = "wss://api-pub.bitfinex.com/ws/2"
        self.symbol = "tBTCUSD"
        self.interval = "1m"
        self.klines = []

    async def process(self, socket: ClientWebSocketResponse):
        async for message in socket:
            message: WSMessage
            if message.type == WSMsgType.TEXT:
                data = message.json()
                try:
                    event = Event(*data)
                except TypeError:
                    data = [0, [1694632440000, 26140, 26140, 26140, 26140, 0.024534]]
                    event = Event(*data)
                self.klines.append(event.kline)
                vwap = calculate_vwap(self.klines)
                response = Response(kline=event.kline, vwap=vwap)
                print(response.model_dump_json())

    async def connect(self, socket: ClientWebSocketResponse):
        key = f"trade:{self.interval}:{self.symbol}"
        handshake = Handshake(key=key)
        await socket.send_str(handshake.model_dump_json())

    async def subscribe(self):
        async with ClientSession().ws_connect(self.url) as socket:
            await self.connect(socket)
            await self.process(socket)
