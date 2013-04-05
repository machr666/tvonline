#!/usr/bin/python

from util.util import *
import abc

class StreamDAO(object):
    """ This is an abstract class for a stream factory """
    __metaclass__ = abc.ABCMeta

    def __init__(self,svrMgr):
        self._svrMgr = svrMgr

    @abc.abstractmethod
    def getStreams(self):
        pass

    def getStreamClass(self,name):
        return getClass(name)

    def getServers(self,servers):
        return [self._svrMgr.getServer(svr) for svr in servers]
