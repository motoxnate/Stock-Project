from setup import *

alphavantage_key = loadAlphavantageKey()
# with open('alphavantage.key') as f:       #Load the API Key
#     alphavantage_key = f.read()
# f.closed

class URL:
    def __init__(self, symbol, interval, apikey=alphavantage_key):
        self.base = """https://www.alphavantage.co/query?"""
        self.function = 'function='
        self.symbol = 'symbol=' + symbol
        self.interval = 'interval=' + interval
        self.time_period = 'time_period='
        self.series_type = 'series_type='
        self.outputsize = 'outputsize='
        self.apikey = 'apikey=' + apikey

class Intraday_URL(URL):
    def __init__(self, symbol, interval, outputsize):
        super(Intraday_URL, self).__init__(symbol, interval)
        self.function += 'TIME_SERIES_INTRADAY'
        self.outputsize += outputsize

    def build(self):
        return(self.base +
        '&'.join((self.function, self.symbol, self.interval, self.outputsize, self.apikey)))

class Daily_URL(URL):
    def __init__(self, symbol, outputsize='compact'):
        super(Daily_URL, self).__init__(symbol, "None")
        self.function += 'TIME_SERIES_DAILY'
        self.outputsize += outputsize

    def build(self):
        return(self.base +
        '&'.join((self.function, self.symbol, self.interval, self.outputsize, self.apikey)))

class RSI_URL(URL):
    def __init__(self, symbol, interval, time_period, series_type):
        super(RSI_URL, self).__init__(symbol, interval)
        self.function += 'RSI'
        self.time_period += time_period
        self.series_type += series_type

    def build(self):
        return(self.base +
        '&'.join((self.function, self.symbol, self.interval, self.time_period, self.series_type, self.apikey)))

class EMA_URL(URL):
    def __init__(self, symbol, interval, time_period, series_type):
        super(EMA_URL, self).__init__(symbol, interval)
        self.function += 'EMA'
        self.time_period = 'time_period=' + time_period
        self.series_type = 'series_type=' + series_type

class SMA_URL(URL):
    def __init__(self, symbol, interval, time_period, series_type):
        super(SMA_URL, self).__init__(symbol, interval)
        self.function += 'SMA'
        self.time_period = 'time_period=' + time_period
        self.series_type = 'series_type=' + series_type

    def build(self):
        return(self.base +
        '&'.join((self.function, self.symbol, self.interval, self.time_period, self.series_type, self.apikey)))
