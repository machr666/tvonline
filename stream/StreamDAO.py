#!/usr/bin/python

from util.util import *
import abc

class StreamDAO(object):
    """ This is an abstract class for a stream factory """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getStreams(self):
        pass

    def getStreamClass(self,name):
        return getClass(name)

    def getServers(self,servers):
        return servers
