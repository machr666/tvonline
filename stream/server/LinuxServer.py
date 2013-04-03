#!/usr/bin/python

# import os
from Server import Server

class LinuxServer(Server):
    """ This class represents a linux server """

    def __init__(self,name,address,uplink,uploadMax):
        super(LinuxServer,self).__init__(name,address,uplink,uploadMax)
