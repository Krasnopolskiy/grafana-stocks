import os

import pandas as pd
from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from pydantic import BaseModel

from schemas.base import BaseResponse

TOKEN = os.environ.get("INFLUXDB_TOKEN")
ORG = "MadDevs"
URL = "http://127.0.0.1:8086"
BUCKET = "MadDevs"


def flatten(model: BaseModel) -> dict:
    json = model.model_dump()
    frame = pd.json_normalize(json)
    flattened = frame.to_dict(orient="records")
    return flattened.pop()


def as_point(response: BaseResponse) -> Point:
    flattened = flatten(response)
    point = Point(response.service).tag("symbol", response.symbol)
    for key, value in flattened.items():
        point.field(key, value)
    return point


async def persist(response: BaseResponse):
    point = as_point(response)
    async with InfluxDBClientAsync(url=URL, token=TOKEN, org=ORG) as client:
        write_api = client.write_api()
        await write_api.write(bucket=BUCKET, org=ORG, record=point)
