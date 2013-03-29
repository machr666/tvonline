#!/usr/bin/python

from Config import Config
from ConfigDAO import ConfigDAO

class MockConfigDAO(ConfigDAO):
    """ This is a mock implementation of the ConfigDAO abstract class """

    def loadConfig(self):
        cfg = Config()
        cfg.audioCodecs = ["MP3","WAV","OGG"]
        cfg.curAudioCodec = "WAV"
        cfg.audioRates = [56,96,128,196,256,312]
        cfg.curAudioRate = 128
        cfg.videoCodecs = ["MPEG-I", "MPEG-II", "DIVx", "XVid", "MP4", "VOB"]
        cfg.curVideoCodec = "MP4"
        cfg.videoRates = [576,648,720,850,1024]
        cfg.curVideoRate = 648
        cfg.videoSizes = [33,50,66,75,100]
        cfg.curVideoSize = 66
        cfg.streamEncryptions = ["None", "AES", "Blowfish", "CSMA"]
        cfg.curStreamEncryption = "AES"
        cfg.genEncryptionKey = ["False","True"]
        cfg.curEncryptionKey = ""
        return cfg

    def saveConfig(self, cfg):
        print("New config")
        print(cfg)
        return True
