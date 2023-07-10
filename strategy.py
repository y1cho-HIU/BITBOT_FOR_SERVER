import params_private as prv
import params_public as pub
import statistics


class Strategy:
    def __init__(self):
        self.now_position = pub.POS_OUT
        self.target_price = -1
        self.loss_price = -1

    @staticmethod
    def get_sma(coin_data):
        """
        :param coin_data: [{time, open, close, volume}, ]
        :return: now_sma for strategy
        """
        close_list = [data['close'] for data in coin_data]
        return round(sum(close_list) / len(close_list), 6)

    @staticmethod
    def _calc_rrr(now_sma, env, rate):
        return round(((rate + 1) * env - now_sma) / rate, 4)

    @staticmethod
    def get_std_dev(coin_data):
        close_list = [data['close'] for data in coin_data]
        return round(statistics.stdev(close_list), 6)

    def set_now_position(self, position):
        """ use in operator class """
        self.now_position = position

    def set_target_price(self, position, now_sma, env_price):
        if position == pub.POS_LONG:
            self.target_price = now_sma
            self.loss_price = env_price - (now_sma - env_price) / prv.rrr_rate
        elif position == pub.POS_SHORT:
            self.target_price = now_sma
            self.loss_price = env_price + (now_sma - env_price) / prv.rrr_rate

    def set_target_price_out(self):
        self.target_price = -1
        self.loss_price = -1

    def envelope_strategy(self, coin_data):
        """ default signal, next_position -> not change """
        signal = False
        next_position = self.now_position

        now_sma = self.get_sma(coin_data)
        std_dev = self.get_std_dev(coin_data)
        now_price = coin_data[-1]['close']
        env_up = round(now_sma + (std_dev * prv.env_weight), 6)
        env_down = round(now_sma - (std_dev * prv.env_weight), 6)

        if self.now_position == pub.POS_OUT:
            if now_price <= env_down:
                next_position = pub.POS_LONG
                signal = True
                self.set_target_price(pub.POS_LONG, now_sma, env_down)
            if now_price >= env_up:
                next_position = pub.POS_SHORT
                signal = True
                self.set_target_price(pub.POS_SHORT, now_sma, env_up)

        elif self.now_position == pub.POS_LONG:
            if (now_price >= self.target_price) | (now_price <= self.loss_price):
                next_position = pub.POS_OUT
                signal = True
                self.set_target_price_out()
        elif self.now_position == pub.POS_SHORT:
            if (now_price <= self.target_price) | (now_price >= self.loss_price):
                next_position = pub.POS_OUT
                signal = True
                self.set_target_price_out()

        """
        signal is True -> trading
        signal is False -> nothing
        """
        return signal, next_position

    def display_target_price(self):
        print(f'target_price : {self.target_price} \t loss_price : {self.loss_price}')

