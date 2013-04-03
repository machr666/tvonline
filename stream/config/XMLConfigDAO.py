#!/usr/bin/python

from Config import Config
from ConfigDAO import ConfigDAO
import xml.etree.ElementTree as ET

class XMLConfigDAO(ConfigDAO):
    """ This is a implementation of the ConfigDAO abstract class which
        uses an XML file to store the data. """

    def __init__(self,folder):
        self.folder = folder

    def loadConfig(self):
        cfg = Config()
        xmlRoot = ET.parse(self.folder+'/config.xml').getroot()

        # Load audio config
        cfg.audioCodecs = [str(codec.text) for codec 
                           in xmlRoot.find('audiocodecs').iter('audiocodec')]
        cfg.curAudioCodec = str(xmlRoot.find('audiocodecs').get('cur'))
        cfg.audioRates  = [int(rate.text) for rate
                           in xmlRoot.find('audiorates').iter('audiorate')]
        cfg.curAudioRate = str(xmlRoot.find('audiorates').get('cur'))

        # Load video config
        cfg.videoCodecs = [str(codec.text) for codec 
                           in xmlRoot.find('videocodecs').iter('videocodec')]
        cfg.curVideoCodec = str(xmlRoot.find('videocodecs').get('cur'))
        cfg.videoRates  = [int(rate.text) for rate
                           in xmlRoot.find('videorates').iter('videorate')]
        cfg.curVideoRate = int(xmlRoot.find('videorates').get('cur'))
        cfg.videoSizes  = [int(size.text) for size
                           in xmlRoot.find('videosizes').iter('videosize')]
        cfg.curVideoSize = int(xmlRoot.find('videosizes').get('cur'))

        # Load stream Config
        cfg.streamEncryptions = [str(enc.text) for enc
                                in xmlRoot.find('streamencryptions')
                                          .iter('streamencryption')]
        cfg.curStreamEncryption = str(xmlRoot.find('streamencryptions')
                                             .get('cur'))
        cfg.curEncryptionKey = str(xmlRoot.find('streamencryptions')
                                          .get('key'))

        return cfg

    def saveConfig(self, cfg):
        # Load current config
        xml = ET.parse(self.folder+'/config.xml')
        xmlRoot = xml.getroot()

        # Update config
        xmlRoot.find('audiocodecs').set('cur',cfg.curAudioCodec)
        xmlRoot.find('audiorates').set('cur',cfg.curAudioRate)
        xmlRoot.find('videocodecs').set('cur',cfg.curVideoCodec)
        xmlRoot.find('videorates').set('cur',cfg.curVideoRate)
        xmlRoot.find('videosizes').set('cur',cfg.curVideoSize)
        xmlRoot.find('streamencryptions').set('cur',cfg.curStreamEncryption)
        xmlRoot.find('streamencryptions').set('key',cfg.curEncryptionKey)

        # Save config
        xml.write(self.folder+'config.xml')

        return True
