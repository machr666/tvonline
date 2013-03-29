#!/usr/bin/python

from Config import Config
import abc

class ConfigDAO(object):
    """ This is an abstract class for config data access objects """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def loadConfig(self):
        """ Load current configuration.
            @return Config object """
        pass

    @abc.abstractmethod
    def saveConfig(self, cfg):
        """ Save configuration.
            @return True iff stored successfully """
        pass

    def persistConfig(self, audioCodec,
                   audioRate, videoCodec,
                   videoRate, videoSize,
                   streamEncryption, genEncryptionKey):
        """ This function checks and prepares the configuration
            values posted by the user and saves them. """
        # Check the new configuration values
        cfg = self.loadConfig()
        if (not audioCodec in cfg.audioCodecs or
            not audioRate in cfg.audioRates or
            not videoCodec in cfg.videoCodecs or
            not videoRate in cfg.videoRates or
            not videoSize in cfg.videoSizes or
            not streamEncryption in cfg.streamEncryptions or
            not genEncryptionKey in cfg.genEncryptionKey):
            return False

        # Store the configuration
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

        return self.saveConfig(cfg)
