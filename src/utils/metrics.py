import pandas as pd
import pandas_ta as pta

from schemas.binance import Kline


def calculate_rsi(klines: list[Kline], length=14) -> float:
    close_prices = [kline.close_price for kline in klines]
    series = pd.Series(close_prices)
    rsi = pta.rsi(series, length=length)
    return float(rsi.iat[-1]) if rsi is not None else 0


def calculate_vwap(klines: list[Kline]) -> float:
    frame = pd.DataFrame([kline.__dict__ for kline in klines])
    frame.index = pd.to_datetime(frame["close_time"], unit="ms")
    vwap = frame.ta.vwap()
    return float(vwap.iat[-1]) if vwap is not None else 0
