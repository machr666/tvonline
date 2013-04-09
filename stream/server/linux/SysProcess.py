import os
import signal
import subprocess
import time

class SysProcess(object):

    MAX_NUM_KILL_TRIES = 3

    def __init__(self):
        self.p = None

    def execute(self,cmd):
        if (self.p != None):
            print('Cannot make multiple calls from SysProcess object')
            return False

        self.p = subprocess.Popen(cmd, shell=True,
                                  preexec_fn=os.setsid,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
        return True

    def isAlive(self):
        if (self.p == None):
            return False
        return self.p.poll() == None

    def kill(self):
        if (self.p == None):
            return True
        print("Killing process group with pid:"+str(self.p.pid))
        os.killpg(self.p.pid, signal.SIGKILL)

        tries = SysProcess.MAX_NUM_KILL_TRIES
        while (self.isAlive() and tries>1): 
            os.killpg(self.p.pid, signal.SIGKILL)
            time.sleep(1)
            tries -= 1

        return not self.isAlive()
