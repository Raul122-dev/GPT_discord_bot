from dotenv import load_dotenv
import os

from db import get_data, insert_data, update_data, delete_data, get_all_data, get_all_data_by_query, get_all_data_by_query_sort, get_all_data_by_query_sort_limit, count_data

import logging
log = logging.getLogger("logger_bot")
log.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
log.addHandler(console_handler)

# ------------------ Database methods ------------------

async def _set_api_key(user_id, api_key):
    data = await insert_data("api_keys", {"user_id": user_id, "api_key": api_key})
    if data:
        return True
    else:
        return False
    
async def _get_api_key(user_id):
    data = await get_data("api_keys", {"user_id": user_id})
    if data:
        return data["api_key"]
    else:
        return None
    
async def _update_api_key(user_id, api_key):
    data = await update_data("api_keys", {"user_id": user_id, "api_key": api_key})
    if data:
        return True
    else:
        return False
    
async def _create_user(user_id, name):
    data = await insert_data("users", {"user_id": user_id, "name": name})
    if data:
        return data
    else:
        return None
    
async def _get_user(user_id):
    data = await get_data("users", {"user_id": user_id})
    if data:
        return data["name"]
    else:
        return None
    
async def _set_last_messages(user_id, messages):
    data = await insert_data("last_messages", {"user_id": user_id, "messages": messages})
    if data:
        return True
    else:
        return False
    
async def _update_last_messages(user_id, messages):
    result = await update_data("last_messages", {"user_id": user_id}, {"messages": messages})
    if result.modified_count > 0:
        return True
    else:
        return False

async def _get_last_messages(user_id):
    data = await get_data("last_messages", {"user_id": user_id})
    if data:
        return data
    else:
        return {}