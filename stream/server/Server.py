#!/usr/bin/python

from util.util import *

import abc

class Server(object):
    """ This abstract class represents a generic stream server """
    __metaclass__ = abc.ABCMeta

    SERVER_CLASS = 'svrclass'
    SERVER_UPLINK = 'uplink'
    SERVER_UPLINK_NAME = 'name'
    # Generic constructor arguments
    SERVER_ARGS = ['name','address','maxStreams','uplink','tvOnlinePort',
                   'tvOnlineSecret']
    UPLINK_ARGS = ['maxUpload']

    STATE = enum(UP='Online', DOWN='Offline', BOOT='Booting')
    def __init__(self,name,address,maxStreams,uplink,tvOnlinePort,
                 tvOnlineSecret,maxUpload):
        self._name = name
        self._address = address
        self._maxStreams = int(maxStreams)
        self._uplink = uplink
        self._tvOnlinePort = int(tvOnlinePort)
        self._tvOnlineSecret = tvOnlineSecret
        self._maxUpload = int(maxUpload)
        self._curUpload = 0
        self._state = Server.STATE.DOWN
        self.updateStateChangeTStamp()
        self._pingTrials = 0

    def __eq__(self,other):
        if other == None:
            return False
        return cmp(self,other)

    def __cmp__(self,other):
        return cmp(self.name, other.name)

    def __str__(self):
        return str(self.name + " Type: " + self.serverType +
               " Addr: " + self.address +
               " Uplink: " + self.uplink +
               " UploadMax: " + str(self.maxUpload) +
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
    def tvOnlinePort(self): return self._tvOnlinePort
    @property
    def tvOnlineSecret(self): return self._tvOnlineSecret
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

    def updateStateChangeTStamp(self):
        self.stateTStamp = getTStamp()

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

    # Boot the remote server
    @abc.abstractmethod
    def startServer(self):
        pass

    # Shutdown the remote server
    @abc.abstractmethod
    def stopServer(self):
        pass

    # Get the status of all streams running on the
    # server. Returns a list with the name of  all
    # streams that are currently running
    @abc.abstractmethod
    def getActiveStreams(self):
        pass

    # Start a new stream
    @abc.abstractmethod
    def startStream(self,cfg):
        pass

    # Stop a stream
    @abc.abstractmethod
    def stopStream(self,cfg):
        pass

