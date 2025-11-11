from datetime import datetime
import json
import httpx
from dotenv import load_dotenv  
import os
from fastapi import FastAPI
from database import intraday_prices, database, create_tables
from contextlib import asynccontextmanager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('aaaa')
    await database.connect()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/intraday')
async def get_intraday_data():
    # intraday_prices.insert().values([])
    data = httpx.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={os.getenv("ALPHA_VANTAGE_API")}").json()
    time_series = data["Time Series (5min)"]

    result = [
        {
            "timestamp": datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
            "open": float(values["1. open"]),
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "close": float(values["4. close"]),
            "volume": int(values["5. volume"])
        }
        for timestamp, values in time_series.items()
    ]
    query = intraday_prices.insert().values(result)
    await database.execute(query)
    return data