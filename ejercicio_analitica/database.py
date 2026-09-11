import os
from typing import AsyncGenerator

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "dev_senior_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "JP1806")

DATABASE_URL = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"

async def get_db() -> AsyncGenerator[psycopg.AsyncConnection, None]:
    
    connection = await psycopg.AsyncConnection.connect(DATABASE_URL, row_factory=dict_row)
    try:
        yield connection
    finally:
        await connection.close()