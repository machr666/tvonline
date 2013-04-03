#!/usr/bin/python

import xml.etree.ElementTree as ET
from ServerDAO import ServerDAO

class XMLServerDAO(ServerDAO):
    """ This is an server factory that gets its data from XML files """

    def __init__(self,folder):
        self.serverXML = folder+'/server.xml'
        self.uplinkXML = folder+'/uplink.xml'

    # Constants
    SERVER = "server"
    SERVER_CLASS = "svrclass"
    NAME = "name"
    ADDRESS = "address"
    UPLINK = "uplink"
    UPLOAD_MAX = "maxupload"

    def getServers(self):
        xmlSvrRoot = ET.parse(self.serverXML).getroot()
        xmlUplRoot = ET.parse(self.uplinkXML).getroot()

        servers = []
        for svr in xmlSvrRoot.iter(XMLServerDAO.SERVER):
            # Let's dynamically load the class definition
            svrClassName = svr.find(XMLServerDAO.SERVER_CLASS).text
            svrClass = self.getServerClass(svrClassName)

            # Retrieve the server information
            name = svr.find(XMLServerDAO.NAME).text
            address = svr.find(XMLServerDAO.ADDRESS).text
            uplink = svr.find(XMLServerDAO.UPLINK).text

            # Retrieve the uplink information
            uploadMax = 0
            for upl in xmlUplRoot.iter(XMLServerDAO.UPLINK):
                if (upl.find(XMLServerDAO.NAME).text == uplink):
                    uploadMax = int(upl.find(XMLServerDAO.UPLOAD_MAX).text)
                    break

            # Add the server to the list of servers
            servers.append(svrClass(name,address,uplink,uploadMax))

        return servers
