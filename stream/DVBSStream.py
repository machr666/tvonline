#!/usr/bin/python

from Stream import Stream

class DVBSStream(Stream):
    """ This class represents a DVB-S stream """

    STREAM_ARGS = ['channels:cur','channels/channel:name,id,cat',
                   'categories/category:name,id']

    def __init__(self,name,servers,cfg,cfgFile,
                 curChannel,channels,categories):
        self._curChannel = curChannel
        self._channels = channels
        self._categories = categories
        super(DVBSStream,self).__init__(name,servers,cfg,cfgFile)

    def __str__(self):
        retVal = super(DVBSStream,self).__str__()
        for cat in self.categories:
            retVal += 'Channels in Category: '+cat['name']+'\n'
            for chan in self.channels:
                if (chan['cat'] == cat['id']):
                    retVal+='\t'+str(chan)+'\n'
        return retVal
    @property
    def curChannel(self): return self._curChannel
    @curChannel.setter
    def curChannel(self,value): self._curChannel = value
    @property
    def channels(self): return self._channels
    @property
    def categories(self): return self._categories

    def applyStreamConfig(self):
        pass
