import datetime
import pprint

import params_public as pub


class MockAccount:
    def __init__(self):
        self.buy_price = -1
        self.win_count = 0
        self.trading_count = 0
        self.now_position = pub.POS_OUT
        self.trading_info = []
        self.total_profit_rate = 1
        self.fee_rate = 0.00004 # 0.04%

    def pos_in(self, position, price):
        """ interface """
        self.now_position = position
        self.buy_price = price

    def pos_out(self, sell_price):
        """ interface """
        profit = -1
        buy_price_with_fee = self.buy_price * (1 - self.fee_rate)
        sell_price_with_fee = sell_price * (1 - self.fee_rate)
        if self.now_position == pub.POS_LONG:
            long_profit = (sell_price_with_fee - buy_price_with_fee) / self.buy_price
            profit = long_profit
            self.total_profit_rate = self.total_profit_rate * (1 + long_profit)
            if self.buy_price < sell_price:
                self.win_count += 1
        elif self.now_position == pub.POS_SHORT:
            short_profit = (buy_price_with_fee - sell_price_with_fee) / self.buy_price
            profit = short_profit
            self.total_profit_rate = self.total_profit_rate * (1 + short_profit)
            if self.buy_price > sell_price:
                self.win_count += 1

        self.trading_info.append({'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                  'position': self.now_position,
                                  'buy_price': self.buy_price,
                                  'sell_price': sell_price,
                                  'profit': profit})

        self.trading_count += 1
        self.now_position = pub.POS_OUT
        self.buy_price = -1

    def display_trading_info(self):
        pprint.pprint(self.trading_info)

    def display_win_rate(self):
        if self.trading_count == 0:
            print("trading count is 0.")
        else:
            print(f'win_rate = {round(self.win_count / self.trading_count * 100, 4)}')
            print(f'total_profit_rate : {self.total_profit_rate}')

    def display_state(self):
        print(f'POS : {self.now_position}, BUY_PRICE : {self.buy_price}')
