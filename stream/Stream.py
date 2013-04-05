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
                     'streamencryptions:cur',
                     'streamencryptions/streamencryption']

    STATE = enum(UP='Running', DOWN='Down')

    def __init__(self,name,servers,cfg,cfgFile):
        self._name = name
        self._servers = servers

        # The generic stream configuration
        self._curAudioCodec = cfg[0][0]['cur']
        self._audioCodecs = cfg[1]
        self._curAudioRate = cfg[2][0]['cur']
        self._audioRates = cfg[3]
        self._curVideoCodec = cfg[4][0]['cur']
        self._videoCodecs = cfg[5]
        self._curVideoRate = cfg[6][0]['cur']
        self._videoRates = cfg[7]
        self._curVideoSize = cfg[8][0]['cur']
        self._videoSizes = cfg[9]
        self._curStreamEncryption = cfg[10][0]['cur']
        self._streamEncryptions = cfg[11]
        self._cfgFile = cfgFile

        # Other
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
                  self.type + '\nServers:\n'
        for svr in self.servers:
            retStr += '\t'+str(svr)+'\t Stream-State: '+self.state[svr]+'\n'
        retStr += 'Config: \n'
        retStr += 'AudioCodec: '+ self.curAudioCodec + '\n'
        retStr += 'AudioRate: '+ self.curAudioRate + ' kbit/s\n'
        retStr += 'VideoCodec: '+ self.curVideoCodec + '\n'
        retStr += 'VideoRate: '+ self.curVideoRate + ' kbit/s\n'
        retStr += 'VideoSize: '+ self.curVideoSize + '%\n'
        retStr += 'StreamEncryption: '+ self.curStreamEncryption + '\n'
        return retStr

    @property
    def type(self): return self.__class__.__name__
    @property
    def name(self): return self._name
    @property
    def servers(self): return self._servers

    # Config
    @property
    def curAudioCodec(self): return self._curAudioCodec
    @curAudioCodec.setter
    def curAudioCodec(self, value): self_curAudioCodec = value
    @property
    def audioCodecs(self): return self._audioCodecs

    @property
    def curAudioRate(self): return self._curAudioRate
    @curAudioRate.setter
    def curAudioRate(self, value): self_curAudioRate = value
    @property
    def audioRates(self): return self._audioRates

    @property
    def curVideoCodec(self): return self._curVideoCodec
    @curVideoCodec.setter
    def curVideoCodec(self, value): self_curVideoCodec = value
    @property
    def videoCodecs(self): return self._videoCodecs

    @property
    def curVideoRate(self): return self._curVideoRate
    @curVideoRate.setter
    def curVideoRate(self, value): self_curVideoRate = value
    @property
    def videoRates(self): return self._videoRates

    @property
    def curVideoSize(self): return self._curVideoSize
    @curVideoSize.setter
    def curVideoSize(self, value): self_curVideoSize = value
    @property
    def videoSizes(self): return self._videoSizes

    @property
    def curStreamEncryption(self): return self._curStreamEncryption
    @curStreamEncryption.setter
    def curStreamEncryption(self, value): self_curStreamEncryption = value
    @property
    def streamEncryptions(self): return self._streamEncryptions

    @property
    def cfgFile(self): return self._cfgFile
    @property
    def state(self): return self._state
    @property
    def lock(self): return self._lock

    def setStreamState(self,server,state):
        if (server in self.state):
            self.state[server] = state

    def getStreamState(self,server):
        if (server in self.state):
            return self.state[server]
        return self.STATE.DOWN

    @abc.abstractmethod
    def applyStreamConfig(self):
        pass
