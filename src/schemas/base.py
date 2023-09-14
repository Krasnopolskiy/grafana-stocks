from pydantic import BaseModel


class BaseKline(BaseModel):
    close_time: int
    open_price: float
    close_price: float
    high_price: float
    low_price: float
    volume: float


class BaseEvent(BaseModel):
    kline: BaseKline


class BaseResponse(BaseModel):
    service: str
    symbol: str
    interval: str
    kline: BaseKline
