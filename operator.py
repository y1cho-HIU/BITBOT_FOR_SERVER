import asyncio
import time

import account
import future_data_getter
import params_public as pub
import params_private as prv
import strategy


class Operator:
    def __init__(self, interval=300):
        self.coin_data = []
        self.interval = interval

        self.data_getter = future_data_getter.FutureDataGetter()
        self.account = account.MockAccount()
        self.strategy = strategy.Strategy()

    def _trading_order(self, next_position):
        """ if signal is True """
        price_info = self.data_getter.get_book_info()

        if next_position == pub.POS_OUT:
            if self.account.now_position == pub.POS_LONG:
                self.account.pos_out(price_info['askPrice'])  # 매도가
            elif self.account.now_position == pub.POS_SHORT:
                self.account.pos_out(price_info['bidPrice'])  # 매수가
        elif next_position == pub.POS_LONG:
            self.account.pos_in(next_position, price_info['bidPrice'])
        elif next_position == pub.POS_SHORT:
            self.account.pos_in(next_position, price_info['askPrice'])
        self.strategy.set_now_position(next_position)

    def _timer(self):
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= self.interval:
                break

            time.sleep(1)

    def execute_trade(self):
        self.coin_data.append(self.data_getter.get_info())
        signal, next_position = self.strategy.envelope_strategy(self.coin_data)
        if signal is True:
            self._trading_order(next_position)

        """ waiting """
        self._timer()

    async def auto_trade(self):
        try:
            while True:
                self.execute_trade()

                await asyncio.sleep(self.interval)
        except KeyboardInterrupt as k:
            # logger
            print("STOP TRADING")

    async def display_trading_info(self):
        """ print trading historical info """
        print("display")

    async def check_keyboard_input(self):
        while True:
            key = await asyncio.get_event_loop().run_in_executor(None, input, "")

            if key == "d":
                await self.display_trading_info()
            elif key == "q":
                asyncio.get_event_loop().stop()

    async def run_trading_and_check_input(self):
        task_auto_trade = asyncio.create_task(self.auto_trade())
        task_check_input = asyncio.create_task(self.check_keyboard_input())

        await asyncio.gather(task_auto_trade, task_check_input)

    def async_run(self):
        asyncio.run(self.run_trading_and_check_input())


op = Operator()
op.async_run()