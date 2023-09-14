from typing import Annotated

from pydantic import Field

from schemas.base import BaseEvent, BaseKline, BaseResponse


class Kline(BaseKline):
    close_time: Annotated[int, Field(alias="T")]
    open_price: Annotated[float, Field(alias="o")]
    close_price: Annotated[float, Field(alias="c")]
    high_price: Annotated[float, Field(alias="h")]
    low_price: Annotated[float, Field(alias="l")]
    volume: Annotated[float, Field(alias="v")]
    closed: Annotated[bool, Field(alias="x")]


class Event(BaseEvent):
    time: Annotated[int, Field(alias="E")]
    kline: Annotated[Kline, Field(alias="k")]


class Response(BaseResponse):
    rsi: float
