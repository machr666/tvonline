#!/usr/bin/python

class Config(object):
    """ This class stores the choices made by users on the config page """ 

    def __str__(self):
        return str("Audio Codec:"+str(self.curAudioCodec)+
               " Rate:"+str(self.curAudioRate)+"kbit/s\n"+
               "Video Codec:"+str(self.curVideoRate)+
               " Rate:"+str(self.curVideoRate)+"kbit/s"+
               " Size:"+str(self.curVideoSize)+"%\n"+
               "Stream encryption:"+str(self.curStreamEncryption)+
               " Key:"+str(self.curEncryptionKey))

    # Audio config
    @property
    def audioCodecs(self): return self._audioCodecs
    @audioCodecs.setter
    def audioCodecs(self, value): self._audioCodecs = value
    @property
    def curAudioCodec(self): return self._curAudioCodec
    @curAudioCodec.setter
    def curAudioCodec(self, value): self._curAudioCodec = value
    @property
    def audioRates(self): return self._audioRates
    @audioRates.setter
    def audioRates(self, value): self._audioRates = value
    @property
    def curAudioRate(self): return self._curAudioRate
    @curAudioRate.setter
    def curAudioRate(self, value): self._curAudioRate = value

    # Video config
    @property
    def videoCodecs(self): return self._videoCodecs
    @videoCodecs.setter
    def videoCodecs(self, value): self._videoCodecs = value
    @property
    def curVideoCodec(self): return self._curVideoCodec
    @curVideoCodec.setter
    def curVideoCodec(self, value): self._curVideoCodec = value
    @property
    def videoRates(self): return self._videoRates
    @videoRates.setter
    def videoRates(self, value): self._videoRates = value
    @property
    def curVideoRate(self): return self._curVideoRate
    @curVideoRate.setter
    def curVideoRate(self, value): self._curVideoRate = value
    @property
    def videoSizes(self): return self._videoSizes
    @videoSizes.setter
    def videoSizes(self, value): self._videoSizes = value
    @property
    def curVideoSize(self): return self._curVideoSize
    @curVideoSize.setter
    def curVideoSize(self, value): self._curVideoSize = value

    # Stream config
    @property
    def streamEncryptions(self): return self._streamEncryptions
    @streamEncryptions.setter
    def streamEncryptions(self, value): self._streamEncryptions = value
    @property
    def curStreamEncryption(self): return self._curStreamEncryption
    @curStreamEncryption.setter
    def curStreamEncryption(self, value): self._curStreamEncryption = value
    @property
    def genEncryptionKey(self): return self._genEncryptionKey
    @genEncryptionKey.setter
    def genEncryptionKey(self, value): self._genEncryptionKey = value
    @property
    def curEncryptionKey(self): return self._curEncryptionKey
    @curEncryptionKey.setter
    def curEncryptionKey(self, value): self._curEncryptionKey = value
