import datetime
import pprint

import params_public as pub
import params_private as prv
import future_data_getter
import strategy
import account

import asyncio


dataGetter = future_data_getter.FutureDataGetter()
myStrategy = strategy.Strategy()
myAccount = account.MockAccount()

coin_data = []
trading_info = []
signal = False
next_position = pub.POS_OUT


def execute_trading():
    """
    1. get_data
    2. put to strategy
    3. trading or not
    4. log trading_info
    """
    global signal, next_position

    make_coin_data()
    signal, next_position = myStrategy.envelope_strategy(coin_data)
    if signal is True:
        trading_order()


def make_coin_data():
    now_data = dataGetter.get_info()
    print(":: GET NOW DATA ::")
    pprint.pprint(now_data)
    if len(coin_data) < prv.sma_period:
        coin_data.append(now_data)
    elif len(coin_data) == prv.sma_period:
        del coin_data[0]
        coin_data.append(now_data)


def log_trading_info(position, price):
    """ time, position, price"""
    trading_info.append({"time": datetime.datetime.now(),
                         "position": position,
                         "price": price})


def trading_order():
    price_info = dataGetter.get_book_info()
    log_price = -1
    if next_position == pub.POS_OUT:

        if myAccount.now_position == pub.POS_LONG:
            myAccount.pos_out(price_info['askPrice'])
            log_price = price_info['askPrice']

        elif myAccount.now_position == pub.POS_SHORT:
            myAccount.pos_out(price_info['bidPrice'])
            log_price = price_info['bidPrice']

    elif next_position == pub.POS_LONG:
        myAccount.pos_in(next_position, price_info['bidPrice'])
        log_price = price_info['bidPrice']

    elif next_position == pub.POS_SHORT:
        myAccount.pos_in(next_position, price_info['askPrice'])
        log_price = price_info['askPrice']

    myStrategy.set_now_position(next_position)
    log_trading_info(next_position, log_price)


async def auto_trade():
    print(f'TRADING START:: {datetime.datetime.now()}')
    try:
        while True:
            execute_trading()
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        print(f'STOP:: {datetime.datetime.now()}')


async def display_trading():
    """ trading info """
    pprint.pprint(trading_info)


async def display_win_rate():
    """ get win_rate """
    myAccount.display_win_rate()


async def display_sma():
    close_list = [data['close'] for data in coin_data]
    print(round(sum(close_list) / len(close_list), 4))


async def display_now_state():
    myAccount.display_state()


async def display_coin_data():
    pprint.pprint(coin_data)


async def display_help():
    print("############# help cmd #############")
    print("# display trading info\t\t --press info or i")
    print("# display now sma info\t\t --press sma or s")
    print("# display win rate info\t\t --press win or w")
    print("# display coin data info\t --press coin or c")
    print("# quit command \t\t\t --press quit or q")


async def check_keyboard_input():
    while True:
        key = await asyncio.get_event_loop().run_in_executor(None, input, "cmd (press help or h): ")
        if key == "info" or key == "i":
            await display_trading()
        elif key == "sma" or key == "s":
            await display_sma()
        elif key == "win" or key == "w":
            await display_win_rate()
        elif key == "state" or key == "n":
            await display_now_state()
        elif key == "coin" or key == "c":
            await display_coin_data()
        elif key == "help" or key == "h":
            await display_help()
        elif key == "quit" or key == "q":
            asyncio.get_event_loop().stop()


async def run_together():
    task_auto_trade = asyncio.create_task(auto_trade())
    task_check_input = asyncio.create_task(check_keyboard_input())

    await asyncio.gather(task_auto_trade, task_check_input)


asyncio.run(run_together())