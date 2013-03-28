#!/usr/bin/python

from UserMgmtDAO import UserMgmtDAO

class MockUserMgmtDAO(UserMgmtDAO):
    """ This is a Mock implementation of MockUserMgmtDAO """

    def __init__(self):
        self.userDB     = { 'machr666' : self.hashPwd('secret'),
                            'bob'      : self.hashPwd('bobssecrte')}
        self.groupDB    = { 'machr666' : ['user','admin'],
                            'bob'      : ['user'] }

    def getUserPwd(self,username):
        if (username in self.userDB):
            return self.userDB[username]
        return []

    def getUserGroups(self,username):
        if (username in self.groupDB):
            return self.groupDB[username]
        return []
