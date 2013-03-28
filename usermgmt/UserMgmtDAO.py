#!/usr/bin/python

import abc
import md5

class UserMgmtDAO(object):
    """ This is an abstract class for user management """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getUserPwd(self,username):
        """ Get user password """
        pass

    @abc.abstractmethod
    def getUserGroups(self,username):
        """ Get all group names that user is a member of """
        pass

    @staticmethod
    def hashPwd(password):
        """ Our standard way of hashing passwords """
        return md5.new(password).digest()

    def isLoginValid(self,username,password):
        """ Encrypt the password and check whether it is matching our db """
        return self.hashPwd(password) in [self.getUserPwd(username)]

    def isMemberOfGroup(self,username,group):
        """ Check if user is member of a particular group """
        return group in self.getUserGroups(username)
