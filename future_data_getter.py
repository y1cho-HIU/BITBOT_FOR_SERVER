import requests


class FutureDataGetter:
    def __init__(self):
        self.base_url = 'https://fapi.binance.com'
        self.kline_endpoint = '/fapi/v1/klines'
        self.book_endpoint = '/fapi/v1/ticker/bookTicker'

    def __get_futures_candlestick_data(self):
        try:
            params = {
                'symbol': 'XRPUSDT',
                'interval': '1m',
                'limit': 2
            }
            response = requests.get(self.base_url + self.kline_endpoint, params=params)
            response.raise_for_status()
            candlestick_data = response.json()
            return candlestick_data
        except requests.exceptions.RequestException as e:
            # logger
            return None

    def __get_futures_ticker(self):
        try:
            params = {
                'symbol': 'XRPUSDT'
            }
            response = requests.get(self.base_url + self.book_endpoint, params=params)
            response.raise_for_status()
            ticker_data = response.json()
            return ticker_data
        except requests.exceptions.RequestException as e:
            # logger
            return None

    def get_info(self):
        """ interface """
        candlestick_data = self.__get_futures_candlestick_data()
        if candlestick_data is not None:
            return {
                "time": candlestick_data[0][0],
                "open": float(candlestick_data[0][1]),
                "close": float(candlestick_data[0][4]),
                "volume": float(candlestick_data[0][5])
            }

    def get_book_info(self):
        """ interface """
        ticker_data = self.__get_futures_ticker()
        if ticker_data is not None:
            return {
                'bidPrice': ticker_data['bidPrice'],
                'askPrice': ticker_data['askPrice']
            }

#dg = FutureDataGetter().get_book_info()
#print(dg)