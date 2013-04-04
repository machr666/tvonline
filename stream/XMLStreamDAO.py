#!/usr/bin/python

from Stream import Stream
import xml.etree.ElementTree as ET
from StreamDAO import StreamDAO

class XMLStreamDAO(StreamDAO):
    """ This is an stream factory that gets its data from XML files """

    def __init__(self,folder):
        self.streamXML = folder+'/stream.xml'
        self.folder = folder+'/'

    # Constants
    STREAM = "stream"

    def __getFromQuery(self,root,query):
        ''' Use simple query language to 
            dynamically parse the XML. Query format
            elem1/elem2/.../elemn:attr1,attr2,... returns
            a list of tuples of the following form
            [(path.text,{attr1: val, attr2: val, ...}),...] or
            [path.text,...] or [{attr1: val,...},...] either
            path of attr are not required'''
        qsplit = query.split(':')
        attrs = []
        if (len(qsplit) == 2):
            attrs = qsplit[1].split(',')

        data = []
        for path in root.findall(qsplit[0]):
            # Get element text if there is any
            text = path.text
            if (text == None):
                text = ''
            text = text.strip()

            # Get element attributes
            d = dict()
            for attr in attrs:
                d[attr] = path.get(attr)
            if (len(d) > 0 and not text == ''):
                data.append((text,d))
            elif (not text == ''):
                data.append(text)
            elif (len(d) > 0):
                data.append(d)
        return data

    def getStreams(self):
        xmlStreamRoot = ET.parse(self.streamXML).getroot()

        streams = []
        for stream in xmlStreamRoot.iter(XMLStreamDAO.STREAM):

            # Load generic stream options
            cfgFile = self.__getFromQuery(stream,Stream.STREAM_CFG)[0]
            xmlCfgRoot = ET.parse(self.folder+cfgFile).getroot()
            cfg = []
            for c in Stream.STREAM_CONFIG:
                cfg.append(self.__getFromQuery(xmlCfgRoot,c))

            # Other generic stream information
            name = self.__getFromQuery(stream,Stream.STREAM_NAME)[0]
            servers = self.getServers(
                    self.__getFromQuery(stream,Stream.STREAM_SERVERS))

            # Let's dynamically load the class definition
            streamClassName = self.__getFromQuery(stream,Stream.STREAM_CLASS)[0]
            streamClass = self.getStreamClass(streamClassName)

            # Load class specific information
            args = []
            for arg in streamClass.STREAM_ARGS:
                args.append(self.__getFromQuery(stream,arg))

            streams.append(streamClass(name,servers,cfg,cfgFile,*args))
            '''
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
        '''
        return streams
