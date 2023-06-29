import asyncio
import datetime
import pprint

import future_data_getter

dataGetter = future_data_getter.FutureDataGetter()
coin_data = []


async def auto_get_data():
    try:
        while True:
            make_coin_data()
            # pprint.pprint(coin_data)
            # print(len(coin_data))
            dt = datetime.datetime.fromtimestamp(coin_data[-1]['time']/1000)
            print(dt.strftime("%Y-%m-%d %H:%M:%S"))
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        print("STOP:: auto_get_data()")


def make_coin_data():
    now_data = dataGetter.get_info()
    if len(coin_data) < 7:
        coin_data.append(now_data)
    elif len(coin_data) == 7:
        del coin_data[0]
        coin_data.append(now_data)


async def display_sma():
    close_list = [data['close'] for data in coin_data]
    print(round(sum(close_list) / len(close_list), 4))


async def check_keyboard_input():
    while True:
        key = await asyncio.get_event_loop().run_in_executor(None, input, "")

        if key == "d":
            await display_sma()
        elif key == "q":
            asyncio.get_event_loop().stop()


async def run_get_and_check():
    task_auto_trade = asyncio.create_task(auto_get_data())
    task_check_input = asyncio.create_task(check_keyboard_input())

    await asyncio.gather(task_auto_trade, task_check_input)

asyncio.run(run_get_and_check())