import asyncio
import json

from telethoncontrollerbot.db.db_main import init_tortoise
from telethoncontrollerbot.db.models import DbUser


def write_bc(data):
    with open(f"bc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, sort_keys=True, default=str, indent=4, ensure_ascii=False)


async def import_data():
    await init_tortoise(password="123123", host="157.230.122.80")
    users = await DbUser.filter(subscription__is_subscribe=True).select_related("account")
    for u in users:
        print(u.account)


if __name__ == "__main__":
    asyncio.run(import_data())
