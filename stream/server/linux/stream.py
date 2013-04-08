#!/usr/bin/python
import time
import popen2
from channels import channels
from stream.Stream import Stream
from stream.DVBStream import DVBStream

def runSilent(cmd):
  print(cmd)
  prog = popen2.Popen3(cmd + " > /dev/null 2>&1")
  return prog

def kill(prog):
  while(prog.poll() < -1):
  	runSilent("kill -9 "+prog.pid)
  	sleep(1)

def streamName(cfg):
  return cfg[Stream.STREAM_NAME]

def streamVLC(cfg):
  name = cfg[Stream.STREAM_NAME]
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
  if (cfg['streamClass'] == 'DVBSStream'):
	print("Start DVB-s stream")
  	channel = DVBSStream.STREAM_CFG_CUR[0]
	vlcParams += 'dvb-s://'+channels[channel]
	port = 4000
	protocol = 'http'

  vlcParams += " --sout '#transcode{acodec='+audioCodec+',ab='+audioRate+',channels=2,samplerate=44100,hq"
  vlcParams += ",vcodec='+videoCodec+',vb='+videoRate+',fps=25,scale=0."+videoSize+"}"
  vlcParams += "std{access,'+protocol+',mux,tex,dst=0.0.0.0:'+port+}' -v"

  prog = runSilent("cvlc "+vlcParams)
  return(name,prog,protocol,port)



