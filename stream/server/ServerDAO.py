#!/usr/bin/python

from util.util import *
import abc

class ServerDAO(object):
    """ This is an abstract class for a server factory """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getServers(self):
        pass

    def getServerClass(self,name):
        return getClass(name)
