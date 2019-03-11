import time
import threading
import json
import http.client
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from url import *

with open('pushsafer.key') as f:       #Load the API Key
    pushsafer_key = f.read()
    pushsafer_key = pushsafer_key.strip('\n')
f.closed

class Symbol():
    def __init__(self, symb):
        self.symb = symb
        self.end = False                                        #End Condition to kill Daemons

        # self.intraday = Intraday(symb, '5min')
        # self.intraday = {'Intraday: 5min': self.get(self.intraday.build())}

        self.updateRSI('60min', '14', 'close')
        self.updateEMA('daily', '20', 'close')

        self.indicators = {'overbought': 80, 'oversold': 20, 'rsi_low': 30, 'rsi_high': 70}
        self.alerts = {'overbought': False, 'oversold': False, 'rsi_low': False, 'rsi_high': False}
        self.monitors = {}

        print(self.RSI)
        print(self.EMA)

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
        data = json.loads(self.threadValue.decode('utf-8'))                 #Load JSON string as a dictionary
        return data

    def updateRSI(self, interval, time_period, series_type):
        t = time.time()
        rsi = RSI_URL(self.symb, interval, time_period, series_type)
        self.RSI = {'RSI: ' + ', '.join((interval, time_period, series_type)): self.get(rsi.build())}   #New dict entry for RSI
        with open(logfile, 'a') as f:
            f.write("Finished RSI update in " + str(time.time()-t) +'\n')
        f.closed

    def updateEMA(self, interval, time_period, series_type):
        t = time.time()
        EMA = EMA_URL(self.symb, interval, time_period, series_type)
        self.EMA = {'EMA: ' + ', '.join((interval, time_period, series_type)): self.get(EMA.build())}   #New dict entry for EMA
        with open(logfile, 'a') as f:
            f.write("Finished EMA update in " + str(time.time()-t) +'\n')
        f.closed

    def setSupport(self, support):  #User input support
        self.support = support
        return None

    def setResistance(self, resistance):    #User input resistance
        self.resistance = resistance
        return None

    def beginRSIMonitor(self, interval='daily', time_period='14', series_type='close'):
        label = 'RSI: '+ ', '.join((interval, time_period, series_type))
        self.monitors[label] = RSIMonitor(self, interval, time_period, series_type)
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
