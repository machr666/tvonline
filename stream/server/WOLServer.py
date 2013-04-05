#!/usr/bin/python

import subprocess

from BaseServer import BaseServer

class WOLServer(BaseServer):
    """ This class represents a stream server that supports Wake-On-LAN.
        Make sure etherwake can be run by the server process. e.g. by
        executing `sudo chmod u+s /usr/sbin/etherwake` """

    # WOLServer specific constructor arguments
    SERVER_ARGS = ['wolAddr','wolMACAddr']

    def __init__(self,name,address,maxStreams,uplink,tvOnlinePort,
                 tvOnlineSecret,maxUpload,wolAddr,wolMACAddr):
        self._wolAddr = wolAddr
        self._wolMACAddr = wolMACAddr
        super(WOLServer,self).__init__(name,address,maxStreams,uplink,
                                       tvOnlinePort,tvOnlineSecret,maxUpload)

    def startServer(self):
        subprocess.call(['etherwake', self._wolMACAddr],
                        stdout=subprocess.PIPE)
