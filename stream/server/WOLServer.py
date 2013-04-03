#!/usr/bin/python

import subprocess

from Server import Server

class WOLServer(Server):
    """ This class represents a stream server that supports Wake-On-LAN """

    # WOLServer specific constructor arguments
    SERVER_ARGS = ['wolAddr','wolMACAddr']

    def __init__(self,name,address,maxStreams,uplink,maxUpload,
                 wolAddr,wolMACAddr):
        self._wolAddr = wolAddr
        self._wolMACAddr = wolMACAddr
        super(WOLServer,self).__init__(name,address,maxStreams,
                                         uplink,maxUpload)

    def startServer(self):
        subprocess.call(['wakeonlan', '-i '+self._wolAddr, 
                         self._wolMACAddr], stdout=subprocess.PIPE)
