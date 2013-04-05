#!/usr/bin/python

from Stream import Stream

import time
import threading

class StreamManager(object):
    """ This class manages all streams """

    SECS_BETWEEN_STATUS_CHECKS = 10

    def __init__(self,streamDAO):
        """ Load all streams and create maps that
            facilitates later request handling """
        self._streams = {stream.name : stream for
                            stream in streamDAO.getStreams()}
        serverStreamTpls = [ (svr,stream) for stream in self.streams \
                                             for svr in stream.servers ]
        self._streamsByServer = {}
        for key, val in serverStreamTpls:
            self._streamsByServer.setdefault(key, []).append(val)

        # Create thread status update Thread
        self._t = threading.Thread(target=self.__updateStreamStatus)
        self._t.daemon = True
        self._t.start()

    @property
    def streams(self):
        """ Get up-to-date information about all streams """
        return self._streams.values()

    def __updateStreamStatus(self):
        """ Since different servers host different streams we
            should request the status of all streams from each
            server once and subsequently update the stream 
            objects """
        while(True):
            for server,streams in self._streamsByServer.items():
                activeStreams = server.getActiveStreams()
                # Update each streams state
                for stream in streams:
                    stream.lock.acquire()
                    stream.state = Stream.STATE.DOWN
                    if (stream in activeStreams):
                        stream.state = Stream.STATE.UP
                    stream.lock.release()

        time.sleep(StreamManager.SECS_BETWEEN_STATUS_CHECKS)

    def getStream(self,name):
        """ Get stream object by name """
        if name in self._streams:
            return self._streams[name]
        return None
"""
    def changeServerState(self,name,state):
        "" Start/Stop servers ""
        server = self.getServer(name)
        if server == None:
            return
        server.changeState(state)

    def getServerUploadCapacity(self,name,update=False):
        "" Check the remaining upload capacity of a given server ""
        server = self.getServer(name)
        if server == None:
            return 0
        ttlUplinkUpload = 0
        for uplink in self.__serversByUplink:
            if (uplink == server.uplink):
                ttlUplinkUpload += server.curUpload
        return server.uploadMax - ttlUplinkUpload"""
