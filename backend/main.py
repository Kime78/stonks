import httpx
from dotenv import load_dotenv  
import os
from fastapi import FastAPI
load_dotenv()

app = FastAPI()

@app.get('/intraday')
def get_intraday_data():
    return  httpx.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={os.getenv("ALPHA_VANTAGE_API")}").json()