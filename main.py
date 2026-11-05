from datetime import datetime
from typing import Optional

import polars as pl
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Sensor Readings API")
FILE = "readings.parquet"


def lazy():
    return pl.scan_parquet(FILE)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/readings")
def list_readings(
    sensor_id: Optional[str] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    limit: int = Query(100, le=1000),
    offset: int = 0,
):
    q = lazy()
    if sensor_id:
        q = q.filter(pl.col("sensor_id") == sensor_id)
    if start:
        q = q.filter(pl.col("timestamp") >= start)
    if end:
        q = q.filter(pl.col("timestamp") <= end)
    df = q.slice(offset, limit).collect()
    return df.to_dicts()


@app.get("/stats")
def stats(sensor_id: Optional[str] = None):
    q = lazy()
    if sensor_id:
        q = q.filter(pl.col("sensor_id") == sensor_id)
    df = q.select(
        pl.len().alias("count"),
        pl.col("temperature").mean().alias("avg_temp"),
        pl.col("temperature").min().alias("min_temp"),
        pl.col("temperature").max().alias("max_temp"),
        pl.col("humidity").mean().alias("avg_humidity"),
    ).collect()
    if df["count"][0] == 0:
        raise HTTPException(404, "No data found")
    return df.to_dicts()[0]


@app.get("/hourly")
def hourly(sensor_id: str):
    df = (
        lazy()
        .filter(pl.col("sensor_id") == sensor_id)
        .group_by_dynamic("timestamp", every="1h")
        .agg(pl.col("temperature").mean().alias("avg_temp"))
        .sort("timestamp")
        .head(48)
        .collect()
    )
    return df.to_dicts()