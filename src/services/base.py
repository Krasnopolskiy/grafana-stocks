from typing import Callable, Type, TypeVar

from loguru import logger

from schemas.base import BaseEvent, BaseKline, BaseResponse
from utils.influx import persist

T = TypeVar('T', bound=BaseResponse)

class BaseService:
    interval: str
    symbol: str

    def __init__(self):
        self.service = self.__class__.__name__.upper()
        self.klines = []

    async def subscribe(self):
        pass

    async def connect(self, *args):
        pass

    def parse(self, *args) -> BaseEvent | None:
        pass

    async def process(self, *args):
        pass

    def calculate_metrics(
        self, kline: BaseKline, handler: Callable[[list[BaseKline]], float]
    ) -> float:
        self.klines.append(kline)
        return handler(self.klines)

    async def send(self, response: Type[T], kline: BaseKline, **kwargs):
        response = response(
            kline=kline,
            symbol=self.symbol,
            interval=self.interval,
            service=self.service,
            **kwargs,
        )
        logger.info(response.model_dump_json())
        await persist(response)
