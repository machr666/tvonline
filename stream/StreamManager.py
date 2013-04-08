#!/usr/bin/python

from Stream import Stream

import time
import threading

class StreamManager(object):
    """ This class manages all streams """

    STREAM = "stream"
    SECS_BETWEEN_STATUS_CHECKS = 10

    def __init__(self,streamDAO):
        """ Load all streams and create maps that
            facilitates later request handling """
        self._streamDAO = streamDAO
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
    def streamDAO(self): return self._streamDAO
    @property
    def streams(self):
        """ Get up-to-date information about all streams """
        return self._streams.values()

    def __updateStreamStatus(self):
        """ Since different servers host different streams we
            should request the status of all streams from each
            server once and subsequently update the stream 
            objects. The server returns a dict with a all active
            streams and their address."""
        while(True):
            for server,streams in self._streamsByServer.items():
                activeStreams = server.getActiveStreams()
                # Update each streams state
                for stream in streams:
                    stream.lock.acquire()
                    stream.setStreamState(server,Stream.STATE.DOWN)
                    if (stream.name in activeStreams):
                        stream.setStreamState(server,Stream.STATE.UP)
                        stream.setStreamAddress(server,activeStreams[stream.name])
                    stream.lock.release()
            time.sleep(StreamManager.SECS_BETWEEN_STATUS_CHECKS)

    def getStream(self,name):
        """ Get stream object by name """
        if name in self._streams:
            return self._streams[name]
        return None

    def configureStream(self,name,cfg):
        stream = self.getStream(name)
        if (stream == None):
            return

        # Apply config
        stream.applyConfig(cfg)

        # Save config
        self.streamDAO.persist(stream)
"""

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
