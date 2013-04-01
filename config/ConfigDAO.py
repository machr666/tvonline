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
                   streamEncryption):
        """ This function checks and prepares the configuration
            values posted by the user and saves them.
            @return (Success(T/F),Msg)"""
        # Check the new configuration values
        cfg = self.loadConfig()
        if (not audioCodec in cfg.audioCodecs or
            not int(audioRate) in cfg.audioRates or
            not videoCodec in cfg.videoCodecs or
            not int(videoRate) in cfg.videoRates or
            not int(videoSize) in cfg.videoSizes or
            not streamEncryption in cfg.streamEncryptions):
            return (False,'Chosen configuration is not supported. '+
                          'Configuration was not saved')

        # Store the configuration
        cfg = Config()
        cfg.curAudioCodec = audioCodec
        cfg.curAudioRate = audioRate
        cfg.curVideoCodec = videoCodec
        cfg.curVideoRate = videoRate
        cfg.curVideoSize = videoSize
        cfg.curStreamEncryption = streamEncryption
        cfg.curEncryptionKey = 'NewKey'

        status = (True,'Successfully saved new configuration.')
        try:
            if(not self.saveConfig(cfg)):
                status = (False,'Failed to save the new configuration.')
        except:
            status = (False,'An error occurred while saving the '+
                            'configuration.')

        return status
