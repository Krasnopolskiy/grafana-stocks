import pandas as pd
import pandas_ta as pta

from schemas.base import BaseKline


def calculate_rsi(records: list[BaseKline], length=14) -> float:
    close_prices = [record.close_price for record in records]
    series = pd.Series(close_prices)
    rsi = pta.rsi(series, length=length)
    return float(rsi.iat[-1]) if rsi is not None else 0


def calculate_vwap(records: list[BaseKline]) -> float:
    frame = pd.DataFrame([record.__dict__ for record in records])
    frame["cumulative_volume"] = frame["volume"].cumsum()
    frame["cumulative_volume_price"] = (
        frame["volume"] * (frame["high_price"] + frame["low_price"] + frame["close_price"]) / 3
    ).cumsum()
    vwap = frame['cumulative_volume_price'] / frame['cumulative_volume']
    return float(vwap.iat[-1]) if vwap is not None else 0
