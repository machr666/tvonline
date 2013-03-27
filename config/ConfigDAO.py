#!/usr/bin/python

from Config import Config
import abc

class ConfigDAO(object):
    """ This is an abstract class for config data access objects """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def loadConfig(self):
        pass

    def persistConfig(self, audioCodec,
                   audioRate, videoCodec,
                   videoRate, videoSize,
                   streamEncryption, genEncryptionKey):
        cfg = Config()
        cfg.curAudioCodec = audioCodec
        cfg.curAudioRate = audioRate
        cfg.curVideoCodec = videoCodec
        cfg.curVideoRate = videoRate
        cfg.curVideoSize = videoSize
        cfg.curStreamEncryption = streamEncryption
        cfg.curEncryptionKey = ""
        if (genEncryptionKey.lower() == "true"):
            cfg.curEncryptionKey = "NewKey"

        self.saveConfig(cfg)

    @abc.abstractmethod
    def saveConfig(self, cfg):
        pass
