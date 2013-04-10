from SysProcess import SysProcess
from channels import channels
from stream.Stream import Stream
from stream.DVBSStream import DVBSStream

class LinuxCommands(object):

    def shutdown(self):
        p = SysProcess()
        return p.execute(['shutdown','-h','1'])

    def getTtlUploadRate(self,devices):
        curTtlUploadBits = 0
        for dev in devices:
            txBitFile = open('/sys/class/net/'+dev+'/statistics/tx_bytes','r')
            curTtlUploadBits += int(txBitFile.read())
            txBitFile.close()
        return curTtlUploadBits

    def streamName(self,cfg):
        return cfg[Stream.STREAM_NAME]

    def startStream(self,cfg):
        name = self.streamName(cfg)
        streamClass = cfg[Stream.STREAM_CLASS]
        audioCodec = cfg[Stream.STREAM_CFG_CUR[0]]
        audioRate = cfg[Stream.STREAM_CFG_CUR[1]]
        videoCodec = cfg[Stream.STREAM_CFG_CUR[2]]
        videoRate = cfg[Stream.STREAM_CFG_CUR[3]]
        videoSize = cfg[Stream.STREAM_CFG_CUR[4]]
        streamEncryption = cfg[Stream.STREAM_CFG_CUR[5]]

        vlcParams = ''
        port = '0'
        protocol = ''
        if (streamClass == 'DVBSStream'):
                print('Start DVB-s stream')
                channel = cfg[DVBSStream.STREAM_CFG_CUR[0]]
                vlcParams += 'dvb-s://'+str(channels[channel])
                port = 4000
                protocol = 'http'

        vlcParams += ' --sout=#transcode{acodec='+str(audioCodec)+',ab='+\
                     str(audioRate)+',channels=2,samplerate=44100,hq'
        vlcParams += ',vcodec='+str(videoCodec)+',vb='+str(videoRate)+\
                     ',fps=25,scale=0.'+str(videoSize)+'}' 
        vlcParams += ':std{access='+str(protocol)+',mux=ts,dst=0.0.0.0:'+\
                     str(port)+'} -v'

        p = SysProcess()
        p.execute(str("cvlc "+vlcParams).split())
        return(name,p,protocol,port)
