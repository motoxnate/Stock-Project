import os
import time
import atexit
from symbol import *
from setup import *

def onExit():
    for i in symbols:
        symbols[i].end = True
    time.sleep(1)
# ----Setup---- #
# Load API Key and begin Log
pushsafer_key = loadApiKey()
logfile = startLog()
atexit.register(onExit)
symbols = {}

symbols['AMD'] = Symbol('AMD')
# test.analyzeRSI()
symbols['AMD'].beginRSIMonitor('60min', '14', 'close')
symbols['AMD'].beginAlertDaemon()

symbols['NVDA'] = Symbol('NVDA')
symbols['NVDA'].beginRSIMonitor('60min', '14', 'close')
symbols['NVDA'].beginAlertDaemon()

while(True):
    time.sleep(10)

print()


# test.beginAlertDaemon()

# test = Symbol('XRX')
# test.beginRSIMonitor('60min')
# test.beginAlertDaemon()
# time.sleep(5)

print("Safe Exit, removing logfile...")
os.remove(logfile)

# notify('Test', 'Houston we have a problem', '', '', '', '', 'a', '', '')
