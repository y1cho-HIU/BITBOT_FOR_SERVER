import params_public as pub


class MockAccount:
    def __init__(self):
        self.buy_price = -1
        self.win_count = 0
        self.trading_count = 0
        self.now_position = pub.POS_OUT

    def pos_in(self, position, price):
        """ interface """
        self.now_position = position
        self.buy_price = price

    def pos_out(self, price):
        """ interface """
        if self.now_position == pub.POS_LONG:
            if self.buy_price < price:
                self.win_count += 1
        elif self.now_position == pub.POS_SHORT:
            if self.buy_price > price:
                self.win_count += 1

        self.trading_count += 1
        self.now_position = pub.POS_OUT
        self.buy_price = -1