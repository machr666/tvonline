import time
import threading
from functools import wraps

from LinuxCommands import LinuxCommands as Commands

SERVER_SECRET = "MyBigFatSecret"
STREAM_ADDRESS = "machr666.no-ip.org"

def checkAuth(f):
    @wraps(f)
    def wrapper(self,*args,**kwds):
        # Ensure that only servers who know this server's
        # secret can execute functions on this stream server
        if (not str(args[0]) == SERVER_SECRET):
            print (str(args[0]) + ' is an invalid secret')
            return [False,"Server secret is wrong"]
        return f(self,*args[1:],**kwds)
    return wrapper

class TVOnlineService(object):
    """ Provides functions that the TV-Online website expects
        Stream servers to have """

    UPLOAD_RATE_CALC_INTVL = 5
    UPLOAD_DEVICES = ['wlan0']

    def __init__(self):
        self.__curUploadRate = 0
        self.__lastTtlUpload = 0
        self.__lock = threading.Lock()
        self.__cmds = Commands()
        self.__streams = {}

        self.__t = threading.Thread(target=self.__monitorUploadRate)
        self.__t.daemon = True
        self.__t.start()

    #---------------------------------------------------- 
    # Monitor and control stream server
    #---------------------------------------------------- 

    def __monitorUploadRate(self):
        """ Continually update the current upload rate in bit/s """
        while(True):
            ttl = self.__cmds.getTtlUploadRate(TVOnlineService.UPLOAD_DEVICES)
            rate = (ttl-self.__lastTtlUpload)/TVOnlineService.UPLOAD_RATE_CALC_INTVL
            self.__lastTtlUpload = ttl
            self.__lock.acquire()
            self.__curUploadRate = rate
            self.__lock.release()
            time.sleep(TVOnlineService.UPLOAD_RATE_CALC_INTVL)

    @checkAuth
    def shutdown(self):
        """ Shut down the server """
        print('Shutting down TVOnline stream server.')
        if (self.__cmds.shutdown()):
            return [True, 'Success: Process launched']
        return [False, 'Error: Failed to launch process']

    @checkAuth
    def curUploadRate(self):
        """ Determine current upload rate in bits """
        self.__lock.acquire()
        rate = self.__curUploadRate
        self.__lock.release()
        return [True, rate]

    #---------------------------------------------------- 
    # Monitor stream processes
    #---------------------------------------------------- 
    @checkAuth
    def activeStreams(self):
        """ Return addresses of all active streams """
        inactive = []
        for name,(proc,address) in self.__streams.items():
            if (not proc.isAlive()): inactive.append(name)
        for name in inactive:
            print ("Stream: "+name+" has stopped")
            del self.__streams[name]

        running = {name : address for name,(proc,address)
                                    in self.__streams.items()}
        print("Currently running streams: "+str(running))
        return [True, running]

    #---------------------------------------------------- 
    # Starting and stopping streams
    #---------------------------------------------------- 
    def __stopOldStream(self,cfg):
        name = self.__cmds.streamName(cfg)
        if (name in self.__streams):
            return self.__streams[name][0].kill()
        return True

    @checkAuth
    def startStream(self,cfg):
        """ Start a new stream """
        if (not self.__stopOldStream(cfg)):
            return [False, 'Error: Failed to terminate current '+
                           'instance of the stream: '+str(cfg)]
        (name, proc, protocol, port, sFile) = self.__cmds.startStream(cfg)
        self.__streams[name] = (proc,str(protocol+'://'+str(STREAM_ADDRESS)+
                                         ':'+str(port)+"/"+str(sFile)))
        return [True, {name : self.__streams[name][1]}]

    @checkAuth
    def stopStream(self, cfg):
        if (self.__stopOldStream(cfg)):
            return [True, 'Success: Stopped stream: '+str(cfg)]
        return [False, 'Error: Could not stop stream: '+str(cfg)]

