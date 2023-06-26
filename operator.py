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

    def execute(self):
        while True:
            """ get_future_data() """
            self.coin_data.append(self.data_getter.get_info())
            if len(self.coin_data) < prv.sma_period:
                continue

            """ get strategy """
            signal, next_position = self.strategy.envelope_strategy(self.coin_data)

            """ trading """
            if signal is True:
                price_info = self.data_getter.get_book_info()
                if next_position == pub.POS_OUT:
                    """ pos_out(price) """
                    if self.account.now_position == pub.POS_LONG:
                        self.account.pos_out(price_info['askPrice']) # 매도가
                    elif self.account.now_position == pub.POS_SHORT:
                        self.account.pos_out(price_info['bidPrice']) # 매수가

                    self.strategy.set_now_position(pub.POS_OUT)
                elif next_position == pub.POS_LONG:
                    """ pos_in(next_position, price) """
                    self.account.pos_in(next_position, price_info['bidPrice'])
                elif next_position == pub.POS_SHORT:
                    self.account.pos_in(next_position, price_info['askPrice'])

                self.strategy.set_now_position(next_position)

            """ waiting """
            time.sleep(self.interval)

op = Operator().execute()
