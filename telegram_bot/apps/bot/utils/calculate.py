import asyncio

import aiohttp

from telegram_bot.config.config import config


async def send_request(session, url):
    async with session.get(url) as res:
        return await res.json()


async def get_info_GST_SOL():
    try:
        url1 = "https://api.huobi.pro/market/trade?symbol=gstusdt"
        url2 = "https://api.huobi.pro/market/trade?symbol=solusdt"
        url3 = "https://api.huobi.pro/market/trade?symbol=gmtusdt"
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in [url1, url2, url3]:
                task = asyncio.create_task(send_request(session, url))
                tasks.append(task)
            result = await asyncio.gather(*tasks)
            response_1, response_2, response_3 = result
        price1_gstusdt = response_1['tick']['data'][0]['price']
        price2_solusdt = response_2['tick']['data'][0]['price']
        price3_gmtusdt = response_3['tick']['data'][0]['price']
        return price1_gstusdt, price2_solusdt, price3_gmtusdt
    except ValueError:
        return False


async def calculate_slipper_profit(_max, _min):
    gst_usdt, sol_usdt, gmt_usdt = await get_info_GST_SOL()
    gst_sol = sol_usdt / gst_usdt

    val = _max - _min
    profit = val - ((val / 100) * 6)


    # usdt_profit = profit * gst_usdt * gst_sol
    # gst_profit = profit * sol_usdt / gst_usdt
    # sol_profit = profit * sol_usdt / sol_usdt
    sol_profit = profit * gst_usdt * gst_sol
    usdt_profit = sol_usdt * sol_profit
    # usdt_profit = profit * sol_profit
    gst_profit = sol_profit / gst_usdt

    return gst_usdt, sol_usdt, gmt_usdt, gst_sol, usdt_profit, gst_profit, sol_profit, profit


async def calculate_mint_profit(msg, data):
    summ = (float(data["gst_usdt"]) * config.bot.COL_GTS) + (config.bot.COL_GMT * float(data["gmt_usdt"]))
    revenue = float(msg) * data["sol_usdt"]
    revenue_val = revenue - (revenue / 100 * 6)
    money = revenue_val - summ
    return money


async def calculate_mint_slipper_profit(msg):
    gst_usdt, sol_usdt, gmt_usdt = await get_info_GST_SOL()
    summ = (float(gst_usdt) * config.bot.COL_GTS) + (float(gmt_usdt) * config.bot.COL_GMT)
    sol_usdt = float(sol_usdt)
    gst_sol = sol_usdt / gst_usdt
    revenue = float(msg) * sol_usdt
    revenue_val = revenue - (revenue / 100 * 6)
    money = revenue_val - summ
    return gst_usdt, sol_usdt, gmt_usdt, gst_sol, money
