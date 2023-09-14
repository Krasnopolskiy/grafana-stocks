from pydantic import BaseModel

from schemas.base import BaseEvent, BaseKline, BaseResponse


class Handshake(BaseModel):
    key: str
    event: str = "subscribe"
    channel: str = "candles"


class Kline(BaseKline):
    def __init__(
        self,
        close_time: int,
        open_price: float,
        close_price: float,
        high_price: float,
        low_price: float,
        volume: float,
    ):
        super().__init__(
            close_time=close_time,
            open_price=open_price,
            close_price=close_price,
            high_price=high_price,
            low_price=low_price,
            volume=volume,
        )


class Event(BaseEvent):
    channel_id: int
    kline: Kline

    def __init__(
        self, channel_id: int, kline: tuple[int, float, float, float, float, float]
    ):
        super().__init__(channel_id=channel_id, kline=Kline(*kline))


class Response(BaseResponse):
    vwap: float
