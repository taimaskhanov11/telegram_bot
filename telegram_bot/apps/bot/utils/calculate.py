import asyncio

import aiohttp

COL_GTS = 100
COL_GMT = 130

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
        price1 = response_1['tick']['data'][0]['price']
        price2 = response_2['tick']['data'][0]['price']
        price3 = response_3['tick']['data'][0]['price']
        return price1, price2, price3
    except ValueError:
        return False


async def calculate_slipper_profit(_max, _min):
    gst_usdt, sol_usdt, gmt_usdt = await get_info_GST_SOL()
    gst_sol = sol_usdt / gst_usdt
    profit = (_max - float(_min)) - (((_max - float(_min)) / 100) * 6)
    usdt_profit = profit * gst_usdt * gst_sol
    gst_profit = (profit * gst_usdt) / gst_usdt
    sol_profit = (profit * gst_usdt) / sol_usdt
    return gst_usdt, sol_usdt, gmt_usdt, gst_sol, usdt_profit, gst_profit, sol_profit, profit

async def calculate_mint_profit(msg,data):
    summ = (float(data["gst_usdt"]) * COL_GTS) + (COL_GMT * float(data["gmt_usdt"]))
    revenue = float(msg) * data["sol_usdt"]
    revenue_val = revenue - (revenue / 100 * 6)
    money = revenue_val - summ
    return money

async def calculate_mint_slipper_profit(msg):
    gst_usdt, sol_usdt, gmt_usdt = await get_info_GST_SOL()
    summ = (float(gst_usdt) * COL_GTS) + (float(gmt_usdt) * COL_GMT)
    sol_usdt = float(sol_usdt)
    gst_sol = sol_usdt / gst_usdt
    revenue = float(msg) * sol_usdt
    revenue_val = revenue - (revenue / 100 * 6)
    money = revenue_val - summ
    return gst_usdt, sol_usdt, gmt_usdt, gst_sol, money

