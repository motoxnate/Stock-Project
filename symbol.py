import time
import threading
import json
import http.client
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from url import *
from threads import *

with open('pushsafer.key') as f:       #Load the API Key
    pushsafer_key = f.read()
    pushsafer_key = pushsafer_key.strip('\n')
f.closed

logfile = 'logs/'+str(time.strftime('%Y-%m-%dT%H-%M-%S'))+'.log'
with open(logfile, 'w') as f:
    f.write('Begin Log File ' + str(time.strftime('%Y-%m-%d %H:%M:%S'))+'\n')
f.closed

class Symbol():
    def __init__(self, symb):
        self.symb = symb
        self.end = False

        self.updateRSI('60min', '14', 'close')
        # self.updateEMA('daily', '20', 'close')

        self.indicators = {'overbought': 80, 'oversold': 20, 'rsi_low': 30, 'rsi_high': 70}
        self.alerts = {'overbought': False, 'oversold': False, 'rsi_low': False, 'rsi_high': False}
        self.monitors = {}

        # print(self.RSI)
        # print(self.EMA)

    def get(self, url):                                         #Downloads the JSON from a given url
        # self.threadValue = None                                 #None until first get completes
        # threads = []
        # t = time.clock()
        # for i in range(20):
        #     threads.append(Fetch(i, url, self))
        #     threads[i].start()
        #
        # while self.threadValue is None:
        #     time.sleep(0.01)
        # print("Fetch took", time.clock()-t)

        self.threadValue = http.client.HTTPResponse.read(urlopen(url))           #Faster option, but less reliable.
        data = json.loads(self.threadValue.decode('utf-8'))                      #Load JSON string as a dictionary
        return data

    def updateIntraday(self, interval, outputsize='compact'):
        intraday = Intraday_URL(self.symb, interval, outputsize)
        self.intraday = self.get(intraday.build())

    def updateDaily(self, outputsize='compact'):
        daily = Daily_URL(self.symb, outputsize)
        self.daily = self.get(daily.build())

    def updateRSI(self, interval, time_period, series_type):
        t = time.time()
        key = 'RSI: ' + ', '.join((interval, time_period, series_type))
        rsi = RSI_URL(self.symb, interval, time_period, series_type)
        rsi = self.get(rsi.build())
        try:
            self.RSI[key] = rsi
        except:
            self.RSI = {key: rsi}   #New dict entry for RSI
        with open(logfile, 'a') as f:
            f.write("Finished RSI update in " + str(time.time()-t) +'\n')
        f.closed

    def updateEMA(self, interval, time_period, series_type):
        t = time.time()
        key = 'EMA: ' + ', '.join((interval, time_period, series_type))
        EMA = EMA_URL(self.symb, interval, time_period, series_type)
        EMA = self.get(EMA.build())
        try:
            self.EMA[key] = EMA
        except:
            self.EMA = {key: EMA}   #New dict entry for EMA
        with open(logfile, 'a') as f:
            f.write("Finished EMA update in " + str(time.time()-t) +'\n')
        f.closed

    def updateSMA(self, interval, time_period, series_type):
        t = time.time()
        key = 'SMA: ' + ', '.join((interval, time_period, series_type))
        SMA = SMA_URL(self.symb, interval, time_period, series_type)
        SMA = self.get(SMA.build())
        try:
            self.SMA[key] = SMA
        except:
            self.SMA = {key: SMA}   #New dict entry for SMA
        with open(logfile, 'a') as f:
            f.write("Finished SMA update in " + str(time.time()-t) +'\n')
        f.closed

    def seriesLength(self, short, long):
        return(min(len(short), len(long)))

    def analyzeEMA(self, interval, time_period_short, time_period_long, series_type):
        print("short")
        self.updateEMA(interval, time_period_short, series_type)
        print("long")
        self.updateEMA(interval, time_period_long, series_type)
        short = 'EMA: ' + ', '.join((interval, time_period_short, series_type))
        long = 'EMA: ' + ', '.join((interval, time_period_long, series_type))
        # print("intraday")
        # self.updateIntraday('30min', 'full')
        print("daily")
        self.updateDaily(outputsize='full')

        print(self.daily)
        shortEMA = [(i, self.EMA[short]['Technical Analysis: EMA'][i]['EMA']) for i in self.EMA[short]['Technical Analysis: EMA']]
        shortEMA = shortEMA[:3000]
        shortEMA.reverse()
        longEMA = [(i, self.EMA[long]['Technical Analysis: EMA'][i]['EMA']) for i in self.EMA[long]['Technical Analysis: EMA']]
        longEMA = longEMA[:3000]
        longEMA.reverse()
        print(self.EMA[short])
        print(shortEMA)
        print(longEMA)
        lastShort = shortEMA[0][1]
        lastLong = longEMA[0][1]
        profit = 0
        realProfit = 0

        if lastShort > lastLong:
            uptrend = True
            buy, realBuy = self.daily['Time Series (Daily)'][shortEMA[0][0]]['4. close'], self.daily['Time Series (Daily)'][shortEMA[0][0]]['4. close']
            # buy, realBuy = self.intraday['Time Series (30min)'][shortEMA[0][0]+":00"]['4. close'], self.intraday['Time Series (30min)'][shortEMA[0][0]+":00"]['4. close']
            print("Buy", buy)
        else:
            uptrend = False

        for i in range(1, len(shortEMA)):
            if shortEMA[i][1] > longEMA[i][1]:
                if uptrend is False:
                    uptrend = True
                    realBuy = self.daily['Time Series (Daily)'][shortEMA[i][0]]['4. close']
                    # realBuy = self.intraday['Time Series (30min)'][shortEMA[i][0]+":00"]['4. close']
                    print(shortEMA[i][0], "Buy", realBuy)

                    buy = shortEMA[i][1]

            elif shortEMA[i][1] < longEMA[i][1]:
                if uptrend is True:
                    uptrend = False
                    realSell = self.daily['Time Series (Daily)'][shortEMA[i][0]]['4. close']
                    # realSell = self.intraday['Time Series (30min)'][shortEMA[i][0]+":00"]['4. close']
                    realProfit += float(realSell)-float(realBuy)
                    print(shortEMA[i][0], "Sell", realSell, "Profit:", realProfit)

                    sell = shortEMA[i][1]
                    profit += float(sell)-float(buy)

        print(profit)
        print(realProfit)

    def analyzeSMA(self, interval, time_period_short, time_period_long, series_type):
        print("short")
        self.updateSMA(interval, time_period_short, series_type)
        print("long")
        self.updateSMA(interval, time_period_long, series_type)
        short = 'SMA: ' + ', '.join((interval, time_period_short, series_type))
        long = 'SMA: ' + ', '.join((interval, time_period_long, series_type))
        print("intraday")
        self.updateIntraday('60min', 'full')
        # print("daily")
        # self.updateDaily(outputsize='full')

        # print(self.daily)
        print(self.intraday)
        shortSMA = [(i, self.SMA[short]['Technical Analysis: SMA'][i]['SMA']) for i in self.SMA[short]['Technical Analysis: SMA']]
        longSMA = [(i, self.SMA[long]['Technical Analysis: SMA'][i]['SMA']) for i in self.SMA[long]['Technical Analysis: SMA']]
        print(self.seriesLength(shortSMA, longSMA))
        seriesLength = self.seriesLength(shortSMA, longSMA)
        print(seriesLength)
        shortSMA, longSMA = shortSMA[:seriesLength], longSMA[:seriesLength]
        shortSMA.reverse()
        longSMA.reverse()
        print(self.SMA[short])
        print(len(shortSMA), shortSMA)
        print(len(longSMA), longSMA)
        lastShort = shortSMA[0][1]
        lastLong = longSMA[0][1]
        profit = 0
        realProfit = 0

        if lastShort > lastLong:
            uptrend = True
            # buy, realBuy = self.daily['Time Series (Daily)'][shortSMA[0][0]]['4. close'], self.daily['Time Series (Daily)'][shortSMA[0][0]]['4. close']
            buy, realBuy = self.intraday['Time Series (60min)'][shortSMA[0][0]+":00"]['4. close'], self.intraday['Time Series (60min)'][shortSMA[0][0]+":00"]['4. close']
            print("Buy", buy)
        else:
            uptrend = False

        for i in range(1, len(shortSMA)):
            if shortSMA[i][1] > longSMA[i][1]:
                if uptrend is False:
                    uptrend = True
                    # realBuy = self.daily['Time Series (Daily)'][shortSMA[i][0]]['4. close']
                    realBuy = self.intraday['Time Series (60min)'][shortSMA[i][0]+":00"]['4. close']
                    print(shortSMA[i][0], "Buy", realBuy)

                    buy = shortSMA[i][1]

            elif shortSMA[i][1] < longSMA[i][1]:
                if uptrend is True:
                    uptrend = False
                    # realSell = self.daily['Time Series (Daily)'][shortSMA[i][0]]['4. close']
                    realSell = self.intraday['Time Series (60min)'][shortSMA[i][0]+":00"]['4. close']
                    realProfit += float(realSell)-float(realBuy)
                    print(shortSMA[i][0], "Sell", realSell, "Profit:", realProfit)

                    sell = shortSMA[i][1]
                    profit += float(sell)-float(buy)

        print(profit)
        print(realProfit)


    def analyzeRSI(self):
        self.updateIntraday('60min', 'full')
        intraday = self.intraday['Time Series (60min)']
        print(intraday)
        rsi = self.RSI['RSI: 60min, 14, close']['Technical Analysis: RSI']
        seriesLength = self.seriesLength(intraday, rsi)
        intraday = intraday[:seriesLength]
        rsi = rsi[:seriesLength]
        print(seriesLength)


    def setSupport(self, support):  #User input support
        self.support = support
        return None

    def setResistance(self, resistance):    #User input resistance
        self.resistance = resistance
        return None

    def beginRSIMonitor(self, interval='daily', time_period='14', series_type='close', alert_interval='60'):
        label = 'RSI: '+ ', '.join((interval, time_period, series_type, alert_interval))
        self.monitors[label] = RSIMonitor(self, interval, time_period, series_type, alert_interval)
        self.monitors[label].start()
        return None

    def beginAlertDaemon(self):
        self.monitors['AlertDaemon'] = AlertDaemon(self)
        self.monitors['AlertDaemon'].start()

    def notify(title, message, sound, vibration, icon, iconcolor, device, url, urltitle, private_key = pushsafer_key):
        url = 'https://www.pushsafer.com/api' # Set destination URL here
        post_fields = {                       # Set POST fields here
    	"t" : title,
    	"m" : message,
    	"s" : sound,
    	"v" : vibration,
    	"i" : icon,
    	"c" : iconcolor,
    	"d" : device,
    	"u" : url,
    	"ut" : urltitle,
    	"k" : private_key
    	}

        request = Request(url, urlencode(post_fields).encode())
        print(urlencode(post_fields))
        json = urlopen(request).read().decode()
        print(json)
