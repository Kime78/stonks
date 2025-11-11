import os

from datetime import datetime
from databases import Database
from sqlalchemy import Float, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL") or ""
database = Database(DATABASE_URL)
metadata = MetaData()
print(DATABASE_URL)
engine = create_async_engine(DATABASE_URL)

async def create_tables():
    """Create tables if they don't exist"""
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

intraday_prices = Table(
    "intraday_prices",
    metadata,
    Column("price_id", Integer, primary_key=True),
    Column("timestamp", DateTime),
    Column("open", Float),
    Column("high", Float),
    Column("low", Float),
    Column("close", Float),
    Column("volume", Integer),
)