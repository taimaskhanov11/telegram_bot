import asyncio
import datetime
import json

from telegram_bot.config.config import config
from telegram_bot.db.db_main import init_tortoise
from telegram_bot.db.models import User


def get_data():
    with open(f"telegram_bot_users.json", "r", encoding="utf-8") as f:
        return json.load(f)


async def import_data():
    await init_tortoise(**config.db.dict())
    data = get_data()
    users = data[2]["data"]
    print(await User.first())
    for user in users:
        data_reg = datetime.datetime.strptime(user["data_reg"], "%Y-%m-%d")
        last_start = datetime.datetime.strptime(user["last_start"], "%Y-%m-%d")
        await  User.get_or_create(
            user_id=user["id"],
            defaults={
                'registered_at': data_reg,
                'use_count': user["col_use"],
                'last_start': last_start,
                'language': 'ru'
            }
        )

if __name__ == "__main__":
    asyncio.run(import_data())
