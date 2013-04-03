#!/usr/bin/python

from Server import Server
import xml.etree.ElementTree as ET
from ServerDAO import ServerDAO

class XMLServerDAO(ServerDAO):
    """ This is an server factory that gets its data from XML files """

    def __init__(self,folder):
        self.serverXML = folder+'/server.xml'
        self.uplinkXML = folder+'/uplink.xml'

    # Constants
    SERVER = "server"
    UPLINK = "uplink"

    def getServers(self):
        xmlSvrRoot = ET.parse(self.serverXML).getroot()
        xmlUplRoot = ET.parse(self.uplinkXML).getroot()

        servers = []
        for svr in xmlSvrRoot.iter(XMLServerDAO.SERVER):
            # Let's dynamically load the class definition
            svrClassName = svr.find(Server.SERVER_CLASS).text
            svrClass = self.getServerClass(svrClassName)

            # Retrieve the server information
            args = []
            for attr in Server.SERVER_ARGS:
                args.append(svr.find(attr).text)

            # Retrieve the uplink information
            uplink = svr.find(Server.SERVER_UPLINK).text
            for upl in xmlUplRoot.iter(Server.SERVER_UPLINK):
                if (upl.find(Server.SERVER_UPLINK_NAME).text == uplink):
                    for attr in Server.UPLINK_ARGS:
                        args.append(upl.find(attr).text)
                    break

            # Retrieve extra information related to the server class type
            for attr in svrClass.SERVER_ARGS:
                args.append(svr.find(attr).text)

            # Add the server to the list of servers
            servers.append(svrClass(*args))

        return servers
