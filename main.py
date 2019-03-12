import os  #Add data directory to working directories
os.chdir(os.getcwd() + '/data')     #Working Directory change to /data
import time
# from tkinter import *
import threading
import json
import http.client
from urllib.request import Request, urlopen
from urllib.parse import urlencode

from url import *
from threads import *
from symbol import *

with open('pushsafer.key') as f:       #Load the API Key
    pushsafer_key = f.read()
    pushsafer_key = pushsafer_key.strip('\n')
f.closed

logfile = 'logs/'+str(time.strftime('%Y-%m-%dT%H-%M-%S'))+'.log'
with open(logfile, 'w') as f:
    f.write('Begin Log File ' + str(time.strftime('%Y-%m-%d %H:%M:%S'))+'\n')
f.closed


test = Symbol('AMD')
#test.analyzeRSI()
test.beginRSIMonitor('60min', '14', 'close')

print()
# test.beginAlertDaemon()
# time.sleep(5)
# test.analyzeSMA('60min', '5', '50', 'close')


# class StartFrame:
#     def __init__(self, master):
#         self.master = master
#         master.title("Test GUI")
#         master.geometry("800x400")
#         self.symbols = {}
#
#         self.label = Label(master, text="Stock Tracker")
#         self.label.pack()
#
#         self.add_symbol = Button(master, text="Add Symbol", command=self.add_symbol)
#         self.add_symbol.pack(side='left')
#
#         self.close_button = Button(master, text="Exit", command=master.quit)
#         self.close_button.pack(side='bottom')
#
#     def add_symbol(self, symb):
#         symbols[symbol] = Symbol(symb)
#
# root = Tk()
# my_gui = StartFrame(root)
# root.mainloop()

# test = Symbol('XRX')
# test.beginRSIMonitor('60min')
# test.beginAlertDaemon()
# time.sleep(5)

print("Safe Exit, removing logfile...")
os.remove(logfile)

# notify('Test', 'Houston we have a problem', '', '', '', '', 'a', '', '')
