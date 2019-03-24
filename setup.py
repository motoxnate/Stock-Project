import os
import time
# Working Directory change to /data
os.chdir(os.getcwd() + '/data')


def loadApiKey():
    with open('pushsafer.key') as f:       # Load the API Key
        key = f.read()
        key = key.strip('\n')
    if not f.closed:
        f.close()
    return key


def loadAlphavantageKey():
    with open('alphavantage.key') as f:
        key = f.read()
    if not f.closed:
        f.close()
    return key


def startLog():
    log = 'logs/'+str(time.strftime('%Y-%m-%dT%H-%M-%S'))+'.log'
    with open(log, 'w') as f:
        f.write('Begin Log File ' + str(time.strftime('%Y-%m-%d %H:%M:%S'))+'\n')
    if not f.closed:
        f.close()
    return log