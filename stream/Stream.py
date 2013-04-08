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
    STREAM_CFG_CUR = ['audioCodecs:cur', 'audioRates:cur',
                      'videoCodecs:cur','videoRates:cur',
                      'videoSizes:cur',
                      'streamEncryptions:cur']

    STREAM_CFG_OPTS = ['audioCodecs/audioCodec','audioRates/audioRate',
                       'videoCodecs/videoCodec','videoRates/videoRate',
                       'videoSizes/videoSize',
                       'streamEncryptions/streamEncryption']

    STATE = enum(UP='Up', DOWN='Down')

    def __init__(self,name,servers,cfgCur,cfgOpts,cfgFile):
        self._name = name
        self._servers = servers
        self._audioCodecs = cfgOpts[0]
        self._audioRates = cfgOpts[1]
        self._videoCodecs = cfgOpts[2]
        self._videoRates = cfgOpts[3]
        self._videoSizes = cfgOpts[4]
        self._streamEncryptions = cfgOpts[5]
        self._addresses = {}
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
    def addresses(self): return self._addresses

    @property
    def cfgFile(self): return self._cfgFile
    @property
    def state(self): return self._state
    @property
    def lock(self): return self._lock

    def setStreamState(self,server,state):
        self.state[server] = state
        if (state == Stream.STATE.DOWN and
            server in self.addresses):
            del self.addresses[server]

    def getStreamState(self,server):
        if (not server in self.state):
            self.state[server] = Stream.STATE.DOWN
        return self.state[server]

    def setStreamAddress(self,server,address):
        self.addresses[server] = address

    def getStreamAddress(self,server):
        self.lock.acquire()
        address = ''
        if (server in self.addresses):
            address = self.addresses[server]
        self.lock.release()
        return address

    @abc.abstractmethod
    def applyConfig(self,cfg):
        # The generic stream configuration
        self.lock.acquire()
        if (cfg[Stream.STREAM_CFG_CUR[0]][0] in self.audioCodecs):
            self._curAudioCodec = cfg[Stream.STREAM_CFG_CUR[0]][0]
        if (cfg[Stream.STREAM_CFG_CUR[1]][0] in self.audioRates):
            self._curAudioRate = cfg[Stream.STREAM_CFG_CUR[1]][0]
        if (cfg[Stream.STREAM_CFG_CUR[2]][0] in self.videoCodecs):
            self._curVideoCodec = cfg[Stream.STREAM_CFG_CUR[2]][0]
        if (cfg[Stream.STREAM_CFG_CUR[3]][0] in self.videoRates):
            self._curVideoRate = cfg[Stream.STREAM_CFG_CUR[3]][0]
        if (cfg[Stream.STREAM_CFG_CUR[4]][0] in self.videoSizes):
            self._curVideoSize = cfg[Stream.STREAM_CFG_CUR[4]][0]
        if (cfg[Stream.STREAM_CFG_CUR[5]][0] in self.streamEncryptions):
            self._curStreamEncryption = cfg[Stream.STREAM_CFG_CUR[5]][0]
        self.lock.release()

        # Apply stream state
        streamCfg = self.getCfg()
        for server in self.servers:
            if server.name in cfg:
                state = cfg[server.name][0]
                self.lock.acquire()
                if (not self.getStreamState(server) == state):
                    self.setStreamState(server,state)
                    if (state == Stream.STATE.UP):
                        server.startStream(streamCfg)
                    else:
                        server.stopStream(streamCfg)
                self.lock.release()

    @abc.abstractmethod
    def getCfg(self):
        self.lock.acquire()
        cfg = { Stream.STREAM_NAME : self.name,
                 Stream.STREAM_CLASS : self.type,
                 Stream.STREAM_CFG_CUR[0] : self.curAudioCodec,
                 Stream.STREAM_CFG_CUR[1] : self.curAudioRate,
                 Stream.STREAM_CFG_CUR[2] : self.curVideoCodec,
                 Stream.STREAM_CFG_CUR[3] : self.curVideoRate,
                 Stream.STREAM_CFG_CUR[4] : self.curVideoSize,
                 Stream.STREAM_CFG_CUR[5] : self.curStreamEncryption }
        self.lock.release()
        return cfg
