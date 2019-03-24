import os
import time
from symbol import *
from setup import *


# ----Setup---- #
# Load API Key
pushsafer_key = loadApiKey()
# Begin Logfile
logfile = startLog()


test = Symbol('AMD')
# test.analyzeRSI()
test.beginRSIMonitor('60min', '14', 'close')

print()

# test.beginAlertDaemon()

# test = Symbol('XRX')
# test.beginRSIMonitor('60min')
# test.beginAlertDaemon()
# time.sleep(5)

print("Safe Exit, removing logfile...")
os.remove(logfile)

# notify('Test', 'Houston we have a problem', '', '', '', '', 'a', '', '')
