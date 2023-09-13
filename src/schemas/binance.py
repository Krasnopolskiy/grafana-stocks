from pydantic import Field

from schemas.base import BaseEvent, BaseKline, BaseResponse


class Kline(BaseKline):
    close_time: int = Field(alias="T")
    open_price: float = Field(alias="o")
    close_price: float = Field(alias="c")
    high_price: float = Field(alias="h")
    low_price: float = Field(alias="l")
    volume: float = Field(alias="v")
    closed: bool = Field(alias="x")


class Event(BaseEvent):
    time: int = Field(alias="E")
    kline: Kline = Field(alias="k")


class Response(BaseResponse):
    service: str = "binance"
    rsi: float
