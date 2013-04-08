from functools import wraps
import subprocess
import threading
import time
import popen2
from channels import channels
from stream.Stream import Stream
from stream.DVBSStream import DVBSStream

SERVER_SECRET = "TVOnlineRules"
STREAM_ADDRESS = "192.168.0.1"

#SERVER_FCTS = ['shutdown','curUploadRate',
#               'activeStreams','startStream',
#               'stopStream']
SERVER_FCTS = []
def serviceFct(f):
    # Register function 
    global SERVER_FCTS
    SERVER_FCTS.append(f.__name__)
    @wraps(f)
    def wrapper(*args, **kwds):
        # Ensure that only servers who know this server's
        # secret can execute functions on this stream server
        if (not str(args[0]) == SERVER_SECRET):
            print (str(args[0]) + ' is an invalid secret')
            return [False,"Server secret is wrong"]
        return f(*args[1:], **kwds)
    return wrapper

# Shutdown the server
@serviceFct
def shutdown():
    print('Shutting down server')
    retVal = subprocess.call(['shutdown','-h','1'],
                             stdout=subprocess.PIPE) == 0
    return [retVal]

# Check the servers upload rate
CALC_ITVL = 5
lastTtlUploadbit = 0
curUpload = 0
def calcUploadRate():
    global lastTtlUploadbit
    global curUpload
    while(True):
        txKbit = open('/sys/class/net/wlan0/statistics/tx_bytes','r')
        curTtlUploadbit = int(txKbit.read())
        txKbit.close()
        curUpload = (curTtlUploadbit - lastTtlUploadbit)/CALC_ITVL
        lastTtlUploadbit = curTtlUploadbit
        time.sleep(CALC_ITVL)

uploadRateThread = threading.Thread(target=calcUploadRate)
uploadRateThread.daemon = True
uploadRateThread.start()

@serviceFct
def curUploadRate():
    """ Return current upload rate in bits """
    #print('UploadRate: '+str(curUpload)+ 'bit/s')
    return curUpload

# Stream management
streams = {}
def inactiveProg(prog):
    print(prog.poll())
    if (prog.poll() == -1):
    	return False
    return True

# Check which streams are up
@serviceFct
def activeStreams():
    # Remove inactive streams
    global streams
    print("Streams: " + str(streams))
    inactive = []
    for stream, (prog,address) in streams.items():
	if (inactiveProg(prog)):
	     inactive.append(stream)
    for stream in inactive:
	print(stream + str(streams[stream]) + "has stopped")
        del streams[stream]

    return {stream : address for stream, (prog,address) in streams.items()}

# Start a new Stream
@serviceFct
def startStream(cfg):
    print("Starting stream: " + str(cfg))
    global streams
    name = streamName(cfg)
    if (name in streams):
    	# Stop stream
	kill(streams[name][0])

    # Start stream
    (name,prog,protocol,port) = streamVLC(cfg)
    streams[name] = (prog,str(protocol)+"://"+str(STREAM_ADDRESS)+":"+str(port))
    return True

# Stop a Stream
@serviceFct
def stopStream(cfg):
    global streams
    name = streamName(cfg)
    if (name in streams):
	return kill(streams[name][0])
    return False

def kill(prog):
    while(prog.poll() == -1):
	runSilent("kill -9 "+ str(prog.pid))
	time.sleep(1)
    return True


def runSilent(cmd):
  print(cmd)
  prog = popen2.Popen3(cmd + " > /dev/null 2>&1")
  return prog

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
  	channel = cfg[DVBSStream.STREAM_CFG_CUR[0]]
	vlcParams += 'dvb-s://'+str(channels[channel])
	port = 4000
	protocol = 'http'

  vlcParams += " --sout '#transcode{acodec="+str(audioCodec)+",ab="+str(audioRate)+",channels=2,samplerate=44100,hq"
  vlcParams += ",vcodec="+str(videoCodec)+",vb="+str(videoRate)+",fps=25,scale=0."+str(videoSize)+"}" 
  vlcParams += "std{access,"+str(protocol)+",mux,tex,dst=0.0.0.0:"+str(port)+"}' -v"

  prog = runSilent("cvlc "+vlcParams)
  return(name,prog,protocol,port)
