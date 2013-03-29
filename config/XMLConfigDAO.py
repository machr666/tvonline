#!/usr/bin/python

from Config import Config
from ConfigDAO import ConfigDAO

class XMLConfigDAO(ConfigDAO):
    """ This is a implementation of the ConfigDAO abstract class which
        uses an XML file to store the data. """

    def loadConfig(self):
        cfg = Config()
        return cfg

    def saveConfig(self, cfg):
        return True
