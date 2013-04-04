from functools import wraps
import subprocess

SERVER_SECRET = "TVOnlineRules"
SERVER_FCTS = ['shutdown']

def requireSecret(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if (not str(args[0]) == SERVER_SECRET):
            print (str(args[0]) + ' is an invalid secret')
            return [False,"Server secret is wrong"]
        return f(*args[1:], **kwds)
    return wrapper

@requireSecret
def shutdown():
    print('Shutting down server')
    retVal = subprocess.call(['shutdown','-h','1'],
                             stdout=subprocess.PIPE) == 0
    return [retVal]
