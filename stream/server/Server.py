#!/usr/bin/python

from util.util import *

import abc
import time
import threading
import subprocess

class Server(object):
    """ This abstract class represents a generic stream server """
    __metaclass__ = abc.ABCMeta

    SERVER_CLASS = 'svrclass'
    SERVER_UPLINK = 'uplink'
    SERVER_UPLINK_NAME = 'name'
    # Generic constructor arguments
    SERVER_ARGS = ['name','address','maxStreams','uplink']
    UPLINK_ARGS = ['maxUpload']

    STATE = enum(UP='Online', DOWN='Offline', BOOT='Booting')
    MAX_PING_TRIAL = 3
    MAX_BOOT_TIME_SECS = 60
    SECS_BETWEEN_STATE_CHECKS = 5

    def __init__(self,name,address,maxStreams,uplink,maxUpload):
        self._name = name
        self._address = address
        self._maxStreams = int(maxStreams)
        self._uplink = uplink
        self._maxUpload = int(maxUpload)
        self._curUpload = 0
        self._state = Server.STATE.DOWN
        self.updateStateChangeTStamp()
        self._pingTrials = 0

        # Let's create background process that regularly checks if
        # the server status
        self._lock = threading.Lock()
        self.__t = threading.Thread(target=self.__checkState)
        self.__t.daemon = True
        self.__t.start()

    def __eq__(self,other):
        if other == None:
            return False
        return cmp(self,other)

    def __cmp__(self,other):
        return cmp(self.name, other.name)

    def __str__(self):
        return str(self.name + " at " + self.address +
               " Uplink: " + self.uplink +
               " UploadMax: " + str(self.uploadMax) +
               " CurUpload: " + str(self.curUpload))

    @property
    def serverType(self): return self.__class__.__name__
    @property
    def name(self): return self._name
    @property
    def address(self): return self._address
    @property
    def maxStreams(self): return self._maxStreams
    @property
    def uplink(self): return self._uplink
    @property
    def maxUpload(self): return self._maxUpload
    @property
    def curUpload(self): return self._curUpload
    @curUpload.setter
    def curUpload(self,value): self._curUpload = value
    @property
    def state(self): return self._state
    @state.setter
    def state(self,value): self._state = value
    @property
    def stateTStamp(self): return self._stateTStamp
    @stateTStamp.setter
    def stateTStamp(self,value): self._stateTStamp = value
    @property
    def pingTrials(self): return self._pingTrials
    @pingTrials.setter
    def pingTrials(self,value): self._pingTrials = value
    @property
    def lock(self): return self._lock
        
    def updateStateChangeTStamp(self):
        self.stateTStamp = getTStamp()

    def __checkState(self):
        """ Check current server state """
        while(True):
            # Has the maximum boot time been exceeded?
            if (self.state == Server.STATE.BOOT and
                getTStamp() - self.stateTStamp >= Server.MAX_BOOT_TIME_SECS):
                self.lock.acquire()
                self.state = Server.STATE.DOWN
                self.lock.release()
            # Server up and running?
            if (subprocess.call(['ping', '-c 1', self.address],
                                stdout=subprocess.PIPE) == 0):
                self.lock.acquire()
                self.state = Server.STATE.UP
                self.pingTrials = 0
                self.lock.release()
            # Ping failure
            else:
                self.lock.acquire()
                self.pingTrials += 1
                if (not self.state == Server.STATE.BOOT and
                    self.pingTrials == Server.MAX_PING_TRIAL):
                    self.state = Server.STATE.DOWN
                self.lock.release()

            # Let's wait a while
            time.sleep(Server.SECS_BETWEEN_STATE_CHECKS)

    def changeState(self,state):
        """ Set server state """
        print(state)
        if (state == Server.STATE.UP):
            print("Booting up " + self.name)
            self.startServer()
            self.lock.acquire()
            self.state = Server.STATE.BOOT
            self.updateStateChangeTStamp()
            self.lock.release()
        elif (state == Server.STATE.DOWN):
            print("Shutting down " + self.name)
            self.stopServer()

    # This process is server dependent and should be implemented by
    # child classes
    @abc.abstractmethod
    def startServer(self):
        pass

    # This should be a feature of the server's TVOnline service
    @abc.abstractmethod
    def stopServer(self):
        pass


class StdServer(Server):
    """ This class represents a generic stream server """

    SERVER_ARGS = []

    def startServer(self):
        pass

    def stopServer(self):
        pass
