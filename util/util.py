#!/usr/bin/python

import time

def enum(**enums):
    return type('Enum', (), enums)

def getClass(name):
    pkgMod = '.'.join(name.split('.')[0:-1])
    clsName = name.split('.')[-1]
    mod = __import__(pkgMod, fromlist=[clsName])
    return getattr(mod, clsName)

def getTStamp():
    return time.time()
