import numpy as np
import polars as pl
from datetime import datetime, timedelta

N = 1_000_000
start = datetime(2026, 1, 1)

df = pl.DataFrame({
"timestamp": [start + timedelta(seconds=10 * i) for i in range(N)],
"sensor_id": np.random.choice(["A1", "A2", "B1", "B2"], N),
"temperature": np.random.normal(22, 3, N).round(2),
"humidity": np.random.normal(50, 8, N).round(2),
})

df.write_parquet("readings.parquet")
print("Done:", df.shape)