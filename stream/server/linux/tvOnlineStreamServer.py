from functools import wraps
import subprocess
import threading
import time
SERVER_SECRET = "TVOnlineRules"
SERVER_FCTS = ['shutdown','curUploadRate']

def requireSecret(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if (not str(args[0]) == SERVER_SECRET):
            print (str(args[0]) + ' is an invalid secret')
            return [False,"Server secret is wrong"]
        return f(*args[1:], **kwds)
    return wrapper

# Shutdown the server
@requireSecret
def shutdown():
    print('Shutting down server')
    retVal = subprocess.call(['shutdown','-h','1'],
                             stdout=subprocess.PIPE) == 0
    return [retVal]

# Check the servers upload rate
CALC_ITVL = 5
lastTtlUploadbit = 0
curUpload = 0
def calcUploadRate():
    global lastTtlUploadbit
    global curUpload
    while(True):
        txKbit = open('/sys/class/net/wlan0/statistics/tx_bytes','r')
        curTtlUploadbit = int(txKbit.read())
        txKbit.close()
        curUpload = (curTtlUploadbit - lastTtlUploadbit)/CALC_ITVL
        lastTtlUploadbit = curTtlUploadbit
        time.sleep(CALC_ITVL)

uploadRateThread = threading.Thread(target=calcUploadRate)
uploadRateThread.daemon = True
uploadRateThread.start()

@requireSecret
def curUploadRate():
    """ Return current upload rate in bits """
    return curUpload
