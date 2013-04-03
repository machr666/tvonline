#!/usr/bin/python



class StreamConfigControl(object):
    """ This class controls the stream configuration """

    def __init__(self,streamsCfgDAO):
        self.streamsCfgDAO = streamsCfgDAO

    @property
    def streams(self): return self.streamsCfgDAO.streams

    def loadStreamCfg(self, streamName):
        """ Get the configuration for a stream by name """
        return self.streamsCfgDAO.getCfg(streamName)

    def saveStreamCfg(self, streamCfg):
        """ Update the configuration for a stream """
        return self.streamsCfgDAO.setCfg(streamCfg)
