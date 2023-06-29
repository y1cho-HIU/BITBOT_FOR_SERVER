import params_private as prv
import params_public as pub


class Strategy:
    def __init__(self, sma_period=prv.sma_period, env_weight=prv.env_weight, rrr_rate=prv.rrr_rate):
        self.sma_period = sma_period
        self.env_weight = env_weight
        self.rrr_rate = rrr_rate
        self.now_position = pub.POS_OUT

    @staticmethod
    def get_sma(coin_data):
        """
        :param coin_data: [{time, open, close, volume}, ]
        :return: now_sma for strategy
        """
        close_list = [data['close'] for data in coin_data]
        return round(sum(close_list) / len(close_list), 4)

    @staticmethod
    def _calc_rrr(now_sma, env, rate):
        return round(((rate + 1) * env - now_sma) / rate, 4)

    def set_now_position(self, position):
        """ use in operator class """
        self.now_position = position

    def envelope_strategy(self, coin_data):
        """ default signal, next_position -> not change """
        signal = False
        next_position = self.now_position

        now_sma = self.get_sma(coin_data)
        now_price = coin_data[-1]['close']
        env_up = round(now_sma * (1 + self.env_weight), 4)
        env_down = round(now_sma * (1 - self.env_weight), 4)
        rrr_up = self._calc_rrr(env_up, now_sma, self.rrr_rate)
        rrr_down = self._calc_rrr(env_down, now_sma, self.rrr_rate)

        if self.now_position == pub.POS_OUT:
            if now_price <= env_down:
                next_position = pub.POS_LONG
                signal = True

            if now_price >= env_up:
                next_position = pub.POS_SHORT
                signal = True

        elif self.now_position == pub.POS_LONG:
            if (now_price >= now_sma) | (now_price <= rrr_down):
                next_position = pub.POS_OUT
                signal = True
        elif self.now_position == pub.POS_SHORT:
            if (now_price <= now_sma) | (now_price >= rrr_up):
                next_position = pub.POS_OUT
                signal = True

        """
        signal is True -> trading
        signal is False -> nothing
        """
        return signal, next_position
