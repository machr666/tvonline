#!/usr/bin/python

from Stream import Stream

class DVBSStream(Stream):
    """ This class represents a DVB-S stream """

    STREAM_ARGS = ['channels:cur','channels/channel:name,id,cat',
                   'categories/category:name,id']

    CHANNEL = "channel"

    def __init__(self,name,servers,cfg,cfgFile,
                 curChannel,channels,categories):
        self._curChannel = curChannel
        self._catChannels = dict()
        for cat in categories:
            l = []
            for chan in channels:
                if (chan['cat'] == cat['id']):
                        l.append(chan['name'])
            self._catChannels[cat['name']] = l

        super(DVBSStream,self).__init__(name,servers,cfg,cfgFile)

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
    def catChannels(self): return self._catChannels

    def applyStreamConfig(self):
        pass
