import threading
import http.client
from urllib.request import Request, urlopen
import time

class Fetch(threading.Thread):
    def __init__(self, threadID, url, parent):
        threading.Thread.__init__(self, daemon=True)
        self.threadID = threadID
        self.url = url
        self.parent = parent

    def run(self):
        data = http.client.HTTPResponse.read(urlopen(self.url))
        if self.parent.threadValue is None:
            self.parent.threadValue = data

class RSIMonitor(threading.Thread):
    def __init__(self, parent, interval, time_period, series_type, alert_interval):
        threading.Thread.__init__(self, name='RSIMonitor'+ ', '.join((interval, time_period, series_type)), daemon=True)
        self.parent = parent
        self.interval = interval
        self.time_period = time_period
        self.series_type = series_type
        self.alert_interval = alert_interval

    def run(self):          #Check if RSI is within predefined bounds and update RSI
        try:
            while self.parent.end is False:
                print("Monitoring RSI")
                current_rsi = float(self.parent.rsi['RSI: '+ ', '.join((self.interval, self.time_period, self.series_type))]['Technical Analysis: RSI'][next(iter(self.parent.rsi['RSI: '+ ', '.join((self.interval, self.time_period, self.series_type))]['Technical Analysis: RSI']))]['RSI'])
                if current_rsi > self.parent.indicators['rsi_high']:   #Begin watching
                    self.parent.alerts['rsi_high'] = True
                else:
                    self.parent.alerts['rsi_high'] = False
                if current_rsi > self.parent.indicators['overbought']:
                    self.parent.alerts['overbought'] = True
                else:
                    self.parent.alerts['overbought'] = False
                if current_rsi < self.parent.indicators['rsi_low']:
                    self.parent.alerts['rsi_low'] = True
                else:
                    self.parent.alerts['rsi_low'] = False
                if current_rsi < self.parent.indicators['oversold']:
                    self.parent.alerts['oversold'] = True
                else:
                    self.parent.alerts['oversold'] = False

                self.parent.updateRSI(self.time_period, self.interval, self.series_type)
                time.sleep(self.alert_interval)   #In seconds
        except KeyError:        #If update fails..
            self.run()

class AlertDaemon(threading.Thread):            #Sends alerts VIA pushsafer
    def __init__(self, parent, alert_interval=30):
        print("Start Alert Daemon")
        threading.Thread.__init__(self, name='AlertDaemon', daemon=True)
        self.parent = parent
        self.alert_interval = alert_interval
        self.last = [self.parent.alerts[i] for i in self.parent.alerts]
        self.alertRank = {'overbought': 1, 'rsi_high': 2, 'rsi_low': 3, 'oversold': 4}

    def run(self):
        while self.parent.end is False:
            print("Alert Daemon Running")
            ind = 0

            # for i in self.parent.alerts:
            #     if i is True:
            #         if self.last[i]

            for i in self.parent.alerts:
                # print(self.parent.alerts[i], self.last[i])
                if self.parent.alerts[i] != self.last[ind] and self.parent.alerts[i] is True:
                    print(i, self.parent.alerts[i])
                    if i == 'overbought':
                        icon = '48'
                        iconColor = 'red'
                    if i == 'oversold':
                        icon = '49'
                        iconColor = 'red'
                    if i == 'rsi_low':
                        icon = '46'
                        iconColor = 'orange'
                    if i == 'rsi_high':
                        icon = '47'
                        iconColor = 'orange'

                    self.parent.notify('Stock Indicator Alert',     #Title
                            ' '.join((self.parent.symb, i)),            #Message
                            '',                         #Sound
                            '',                         #Vibration
                            icon,                       #Icon
                            iconColor,                      #Iconcolor
                            'a',                        #Device
                            '',                         #URL
                            '')                         #URLTitle

                self.last[ind] = self.parent.alerts[i]
                ind += 1
            time.sleep(1)
