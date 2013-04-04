#!/usr/bin/python

from util.util import *

import abc
import threading

class Stream(object):
    """ This abstract class represents a generic stream """
    __metaclass__ = abc.ABCMeta

    STREAM_NAME = 'name'
    STREAM_CLASS = 'streamClass'
    STREAM_SERVERS = 'servers/server'
    STREAM_CFG = 'streamConfig'
    STREAM_CONFIG = ['audiocodecs:cur','audiocodecs/audiocodec',
                     'audiorates:cur','audiorates/audiorate',
                     'videocodecs:cur','videocodecs/videocodec',
                     'videorates:cur','videorates/videorate',
                     'videosizes:cur','videosizes/videosize',
                     'streamencryptions:cur,key',
                     'streamencryptions/streamencryption']

    STATE = enum(UP='Running', DOWN='Down')

    def __init__(self,name,servers,cfg,cfgFile):
        self._name = name
        self._servers = servers
        self._cfg = cfg
        self._cfgFile = cfgFile
        self._state = {server : Stream.STATE.DOWN for server in servers}
        self._lock = threading.Lock()

    def __eq__(self,other):
        if other == None:
            return False
        return cmp(self,other)

    def __cmp__(self,other):
        return cmp(self.name, other.name)

    def __str__(self):
        retStr = 'Stream: '+ self.name + ' Type: ' +\
                  self.streamType + '\nServers:\n'
        for svr in self.servers:
            retStr += '\t'+str(svr)+'\t Stream-State: '+self.state[svr]+'\n'
        retStr += 'Config: \n'
        for cfg in self.cfg:
            retStr += '\t'+str(cfg)+'\n'
        return retStr

    @property
    def streamType(self): return self.__class__.__name__
    @property
    def name(self): return self._name
    @property
    def servers(self): return self._servers
    @property
    def cfg(self): return self._cfg
    @property
    def cfgFile(self): return self._cfgFile
    @property
    def state(self): return self._state
    @state.setter
    def state(self,value): self._state = value
    @property
    def lock(self): return self._lock

    @abc.abstractmethod
    def streamConfigInfo(self):
        pass

    @abc.abstractmethod
    def applyStreamConfig(self):
        pass
