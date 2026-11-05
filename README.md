# parquet-api

A small FastAPI service that serves a large time-series Parquet file of sensor readings. It uses polars lazy loading, so only the rows and columns a request needs are read, and the full file is never loaded into memory.

## Features

- List readings with filters for sensor, start time and end time
- Pagination with limit and offset
- Summary statistics: count, average, minimum and maximum temperature, average humidity
- Hourly averages per sensor using dynamic grouping
- Interactive API docs generated automatically by FastAPI

## Tech stack

- Python 3.13
- FastAPI and Uvicorn
- polars (lazy scanning of Parquet)
- NumPy (sample data generation)

## Getting started

### 1. Clone and set up the environment

```powershell
git clone https://github.com/StefanNajdoskii/parquet-api.git
cd parquet-api
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS or Linux, activate with `source .venv/bin/activate` instead.

### 2. Generate the sample data

```bash
python generate_data.py
```

This creates `readings.parquet` with one million rows: timestamp, sensor_id, temperature and humidity.

### 3. Run the API

```bash
uvicorn main:app --reload
```

Open http://localhost:8000/docs to try every endpoint in the browser.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | /health | Health check |
| GET | /readings | List readings, with optional sensor_id, start, end, limit and offset |
| GET | /stats | Summary statistics, optionally for one sensor |
| GET | /hourly | Hourly average temperature for one sensor |

### Example requests

```bash
curl "http://localhost:8000/readings?sensor_id=A1&limit=5"
curl "http://localhost:8000/stats?sensor_id=B2"
curl "http://localhost:8000/hourly?sensor_id=A1"
```

## Why lazy loading?

With `pl.scan_parquet`, polars builds a query plan first and runs it only when `.collect()` is called. Filters and column selection are pushed down to the file reader, so a request for one sensor reads only the data it needs. This keeps memory use low and responses fast, even with large files.

## Project structure

```
parquet-api/
generate_data.py creates the sample Parquet file
main.py FastAPI application and endpoints
requirements.txt Python dependencies
```

## Ideas for next steps

- Docker image for easy deployment
- Tests with pytest and FastAPI's TestClient
- Pydantic response models
- Compare performance with DuckDB
- Authentication and a real database for metadata

## Author

Stefan Najdoski, GitHub
