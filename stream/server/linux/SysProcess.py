import os
import signal
import subprocess
import time

class SysProcess(object):

    MAX_NUM_KILL_TRIES = 3

    def __init__(self):
        self.p = None

    @property
    def pid(self):
        if (self.p == None):
            return 0
        return self.p.pid

    def execute(self,cmd):
        if (self.p != None):
            print('Cannot make multiple calls from SysProcess object')
            return False
        print('Starting '+str(cmd))
        self.p = subprocess.Popen(cmd, shell=False,
                                  preexec_fn=os.setsid)
        return True

    def isAlive(self):
        if (self.p == None):
            return False
        return self.p.poll() == None
   
    @staticmethod
    def findAllPids(progName):
        pids = subprocess.Popen(["pidof", progName], stdout=subprocess.PIPE).communicate()[0]
        return [int(pid) for pid in pids.split()]

    @staticmethod
    def killAll(pids):
        for pid in pids:
            SysProcess.killGroup(pid)

    @staticmethod 
    def killGroup(pid):
        print("Killing process group with pid: "+str(pid))
        os.kill(pid, signal.SIGKILL)
        os.killpg(pid, signal.SIGKILL)

    def kill(self):
        if (self.p == None):
            return True
        SysProcess.killGroup(self.p.pid)

        tries = SysProcess.MAX_NUM_KILL_TRIES
        while (self.isAlive() and tries>1): 
            SysProcess.killGroup(self.p.pid)
            time.sleep(1)
            tries -= 1

        return not self.isAlive()
