#!/usr/bin/python

class ServerManager(object):
    """ This class manages the server infrastructure """

    SERVER = "server"
    STATE = "state"

    def __init__(self,serverDAO):
        """ Load all servers and create maps that
            facilitate later request handling """
        self.__servers = {server.name : server for
                            server in serverDAO.getServers()}
        uplinkServerTpls = [(server.uplink, server) for
                                server in self.__servers.values()]
        self.__serversByUplink = {}
        for key, val in uplinkServerTpls:
            self.__serversByUplink.setdefault(key, []).append(val)

    @property
    def infrastructure(self):
        """ Get up-to-date information about all servers """
        return self.__serversByUplink

    def getServer(self,name):
        """ Get server object by name """
        if name in self.__servers:
            return self.__servers[name]
        return None

    def changeServerState(self,name,state):
        """ Start/Stop servers """
        server = self.getServer(name)
        if server == None:
            return
        server.changeState(state)

    def getServerUploadCapacity(self,name,update=False):
        """ Check the remaining upload capacity of a given server """
        server = self.getServer(name)
        if server == None:
            return 0
        ttlUplinkUpload = 0
        for uplink in self.__serversByUplink:
            if (uplink == server.uplink):
                ttlUplinkUpload += server.curUpload
        return server.uploadMax - ttlUplinkUpload
