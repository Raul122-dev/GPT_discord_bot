# db.py
import motor.motor_asyncio
from typing import Any

from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI = os.getenv("MONGO_DB_URI")  # Reemplaza con tu URI de conexión a MongoDB

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client["code_db"]  # Reemplaza con el nombre de tu base de datos


async def get_data(collection: str, query: Any) -> Any:
    result = await db[collection].find_one(query)
    return result


async def insert_data(collection: str, data: Any) -> Any:
    result = await db[collection].insert_one(data)
    return result

async def update_data(collection: str, query: Any, update: Any) -> Any:
    result = await db[collection].update_one(query, {"$set": update})
    return result

async def delete_data(collection: str, data: Any) -> Any:
    result = await db[collection].delete_one(data)
    return result

async def get_all_data(collection: str) -> Any:
    result = await db[collection].find()
    return result

async def get_all_data_by_query(collection: str, query: Any) -> Any:
    result = await db[collection].find(query)
    return result

async def get_all_data_by_query_sort(collection: str, query: Any, sort: Any) -> Any:
    result = await db[collection].find(query).sort(sort)
    return result

async def get_all_data_by_query_sort_limit(collection: str, query: Any, sort: Any, limit: int) -> Any:
    result = await db[collection].find(query).sort(sort).limit(limit)
    return result

async def count_data(collection: str, query: Any) -> Any:
    result = await db[collection].count_documents(query)
    return result