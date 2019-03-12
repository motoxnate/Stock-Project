import threading
import http.client
from urllib.request import Request, urlopen
import time
from alerts import *

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
        self.name = name='RSIMonitor'+ ', '.join((interval, time_period, series_type))
        self.parent = parent
        self.interval = interval
        self.time_period = time_period
        self.series_type = series_type
        self.alert_interval = alert_interval
        self.alert = None

    def run(self):          #Check if RSI is within predefined bounds and update RSI
        try:
            while self.parent.end is False:
                current_rsi = float(self.parent.rsi['RSI: '+ ', '.join((self.interval, self.time_period, self.series_type))]['Technical Analysis: RSI'][next(iter(self.parent.rsi['RSI: '+ ', '.join((self.interval, self.time_period, self.series_type))]['Technical Analysis: RSI']))]['RSI'])
                print("Monitoring RSI\n")

                #Set Alert Status
                if current_rsi >= self.parent.indicators['Overbought']:
                    self.alert = Overbought(self.parent.indicators['Overbought'])
                elif current_rsi >= self.parent.indicators['rsiHigh']:
                    self.alert = RsiHigh(self.parent.indicators['rsiHigh'])
                elif current_rsi > self.parent.indicators['rsiLow']:
                    self.alert = RsiNormal()
                elif current_rsi > self.parent.indicators['Oversold']:
                    self.alert = RsiLow(self.parent.indicators['rsiLow'])
                else:
                    self.alert = Oversold(self.parent.indicators['Oversold'])

                #Write current rsi and alert status back to parent
                self.parent.current_rsi = current_rsi
                self.parent.alerts[self.name] = self.alert
                print(current_rsi)

                self.parent.updateRSI(self.time_period, self.interval, self.series_type)
                time.sleep(float(self.alert_interval))   #In seconds
        except KeyError:        #If update fails try again
            print('Waiting on RSI Update')
            time.sleep(0.5)
            self.run()

class AlertDaemon(threading.Thread):            #Sends alerts VIA pushsafer
    def __init__(self, parent, alert_interval=30):
        print("Start Alert Daemon")
        threading.Thread.__init__(self, name='AlertDaemon', daemon=True)
        self.parent = parent
        self.alert_interval = alert_interval
        self.last = [self.parent.alerts[i] for i in self.parent.alerts]
        self.alertRank = {'Overbought': 1, 'rsiHigh': 2, 'rsiLow': 3, 'Oversold': 4}

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
                    if i == 'Overbought':
                        icon = '48'
                        iconColor = 'red'
                    if i == 'Oversold':
                        icon = '49'
                        iconColor = 'red'
                    if i == 'rsiLow':
                        icon = '46'
                        iconColor = 'orange'
                    if i == 'rsiHigh':
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
