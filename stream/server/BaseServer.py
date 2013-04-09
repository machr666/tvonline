#!/usr/bin/python

from util.util import *
from Server import Server

import time
import xmlrpclib
import threading

class BaseServer(Server):
    """ This class represents a generic stream server """

    SERVER_ARGS = []
    MAX_PING_TRIAL = 3
    MAX_BOOT_TIME_SECS = 60
    SECS_BETWEEN_STATE_CHECKS = 5

    def __init__(self,name,address,maxStreams,uplink,tvOnlinePort,
                 tvOnlineSecret,maxUpload):
        super(BaseServer,self).__init__(name,address,maxStreams,uplink,
                                       tvOnlinePort,tvOnlineSecret,maxUpload)

        # Let's create background process that regularly checks if
        # the server status
        self._lock = threading.Lock()
        self.__t = threading.Thread(target=self.__checkState)
        self.__t.daemon = True
        self.__t.start()

    @property
    def server(self): return xmlrpclib.Server('https://'+self.address+":"+
                                              str(self.tvOnlinePort))
    @property
    def lock(self): return self._lock

    def __checkState(self):
        """ Check current server state """
        while(True):
            # Has the maximum boot time been exceeded?
            if (self.state == Server.STATE.BOOT and
                getTStamp() - self.stateTStamp >= 
                    BaseServer.MAX_BOOT_TIME_SECS):
                self.lock.acquire()
                self.state = Server.STATE.DOWN
                self.lock.release()
            # Server up and running?
            if (self.__getCurUploadRate()):
                self.lock.acquire()
                self.state = Server.STATE.UP
                self.pingTrials = 0
                self.lock.release()
            # Ping failure
            else:
                self.lock.acquire()
                self.pingTrials += 1
                if (not self.state == Server.STATE.BOOT and
                    self.pingTrials == BaseServer.MAX_PING_TRIAL):
                    self.state = Server.STATE.DOWN
                self.lock.release()

            # Let's wait a while
            time.sleep(BaseServer.SECS_BETWEEN_STATE_CHECKS)

    def __getCurUploadRate(self):
        resp = [False,0]
        try:
            # Returns [True,rate]
            resp = self.server.curUploadRate(self.tvOnlineSecret)
            if (resp[0]):
                uploadRate = resp[1]
        except:
            uploadRate = 0
        self.lock.acquire()
        self.curUpload = uploadRate/1024
        self.lock.release()

        return resp[0]

    def startServer(self):
        pass

    def __shutdown(self):
        retVal = False
        try:
            resp = self.server.shutdown(self.tvOnlineSecret)
            retVal = resp[0]
            if (not retVal):
                print(resp[1])
        except Exception, e:
            print(e)
        return retVal

    def stopServer(self):
        # Let spawn a process that executes the remote shutdown
        t = threading.Thread(target=self.__shutdown)
        t.daemon = True
        t.start()

    def getActiveStreams(self):
        retVal = {}
        try:
            # Response is [T/F,{name : address,...}]
            resp = self.server.activeStreams(self.tvOnlineSecret)
            if (resp[0]):
                retVal = resp[1]
            else:
                print (resp[1])
        except Exception, e:
            print(e)
        return retVal

    def __startStream(self,cfg):
        print("Starting stream with args "+str(cfg))
        retVal = False
        try:
            resp = self.server.startStream(self.tvOnlineSecret,cfg)
            retVal = resp[0]
            if (not retVal):
                print (resp[1])
        except Exception, e:
            print(e)
        return retVal

    def startStream(self,cfg):
        t = threading.Thread(target=self.__startStream,args=(cfg,))
        t.daemon = True
        t.start()

    def __stopStream(self,cfg):
        print("Stopping stream with args "+str(cfg))
        retVal = False
        try:
            resp = self.server.stopStream(self.tvOnlineSecret,cfg)
            retVal = resp[0]
            if (not retVal):
                print (resp[1])
        except Exception, e:
            print(e)
        return retVal

    def stopStream(self,cfg):
        t = threading.Thread(target=self.__stopStream,args=(cfg,))
        t.daemon = True
        t.start()
