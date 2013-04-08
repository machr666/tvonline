#!/usr/bin/python

from Stream import Stream

class DVBSStream(Stream):
    """ This class represents a DVB-S stream """

    STREAM_CFG_CUR  = ['channels:cur']
    STREAM_CFG_OPTS = ['channels/channel:name,id,cat',
                       'categories/category:name,id']

    def __init__(self,name,servers,cfgCur,cfgOpts,cfgFile,
                 channels,categories):
        self._channels = []
        self._catChannels = dict()
        for cat in categories:
            l = []
            for chan in channels:
                if (chan['cat'] == cat['id']):
                        l.append(chan['name'])
                        self._channels.append(chan['name'])
            self._catChannels[cat['name']] = l

        # Store current config in object
        super(DVBSStream,self).__init__(name,servers,cfgCur,cfgOpts,cfgFile)

    def __str__(self):
        retVal = super(DVBSStream,self).__str__()
        for cat, channels in self.catChannels.items():
            retVal += 'Channels in Category: '+cat+'\n'
            for chan in channels:
                    retVal+='\t'+chan+'\n'
        return retVal

    @property
    def curChannel(self): return self._curChannel
    @curChannel.setter
    def curChannel(self,value): self._curChannel = value
    @property
    def channels(self): return self._channels
    @property
    def catChannels(self): return self._catChannels

    def applyConfig(self,cfg):
        super(DVBSStream,self).applyConfig(cfg)
        if (cfg[DVBSStream.STREAM_CFG_CUR[0]][0] in self.channels):
            self.curChannel = cfg[DVBSStream.STREAM_CFG_CUR[0]][0]

    def getCfg(self):
        cfg = super(DVBSStream,self).getCfg()
        cfg[DVBSStream.STREAM_CFG_CUR[0]] = self.curChannel
        return cfg
