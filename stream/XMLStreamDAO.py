#!/usr/bin/python

from Stream import Stream
import xml.etree.ElementTree as ET
from StreamDAO import StreamDAO

class XMLStreamDAO(StreamDAO):
    """ This is an stream factory that gets its data from XML files """

    def __init__(self,svrMgr,folder):
        super(XMLStreamDAO,self).__init__(svrMgr)
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
        ''' Load the stream configuration from XML files '''
        xmlStreamRoot = ET.parse(self.streamXML).getroot()

        streams = []
        for stream in xmlStreamRoot.iter(XMLStreamDAO.STREAM):

            # Generic stream information
            name = self.__getFromQuery(stream,Stream.STREAM_NAME)[0]
            servers = self.getServers(
                    self.__getFromQuery(stream,Stream.STREAM_SERVERS))

            # Let's dynamically load the stream class definition
            streamClassName = self.__getFromQuery(stream,Stream.STREAM_CLASS)[0]
            streamClass = self.getStreamClass(streamClassName)

            # Load current stream config
            cfgFile = self.__getFromQuery(stream,Stream.STREAM_CFG)[0]
            xmlCfgRoot = ET.parse(self.folder+cfgFile).getroot()
            cfgCur = dict()
            for c in Stream.STREAM_CFG_CUR:
                cfgCur[c] = [self.__getFromQuery(xmlCfgRoot,c)[0]['cur']]
            for c in streamClass.STREAM_CFG_CUR:
                cfgCur[c] = [self.__getFromQuery(xmlCfgRoot,c)[0]['cur']]

            # Get available config options
            cfgOpts = []
            for c in Stream.STREAM_CFG_OPTS:
                cfgOpts.append(self.__getFromQuery(xmlCfgRoot,c))
            clsCfgOpts = []
            for c in streamClass.STREAM_CFG_OPTS:
                clsCfgOpts.append(self.__getFromQuery(xmlCfgRoot,c))

            # Create the new stream
            streams.append(streamClass(name,servers,cfgCur,cfgOpts,cfgFile,
                           *clsCfgOpts))
        return streams

    def __setFromQuery(self,root,query,value):
        ''' Replace the current attribute pointed to
            by the query with value query must have the
            form path:attr'''
        qsplit = query.split(':')
        for path in root.findall(qsplit[0]):
            path.set(qsplit[1],value)

    def persist(self,stream):
        ''' Save the configutation of the stream to XML '''
        xmlCfgTree = ET.parse(self.folder+stream.cfgFile)
        xmlCfgRoot = xmlCfgTree.getroot()

        for k,v in stream.getCfg().items():
            print(k,v)
            self.__setFromQuery(xmlCfgRoot,k,v)

        xmlCfgTree.write(self.folder+stream.cfgFile)
