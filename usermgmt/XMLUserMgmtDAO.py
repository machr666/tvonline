#!/usr/bin/python

from UserMgmtDAO import UserMgmtDAO

import xml.etree.ElementTree as ET

class XMLUserMgmtDAO(UserMgmtDAO):
    """ This is a XML implementation of UserMgmtDAO """

    def __init__(self,folder):
        xmlUserRoot = ET.parse(folder+"/user.xml").getroot()

        self.__userDB = {}
        self.__groupDB = {}

        for user in xmlUserRoot.iter('user'):
            name = user.get('name')
            self.__userDB[name] = user.get('pwd')
            self.__groupDB[name] = []

            for group in user.findall('groups/group'):
                self.__groupDB[name].append(group.get(name))

    def getUserPwd(self,username):
        if (username in self.__userDB):
            return self.__userDB[username]
        return []

    def getUserGroups(self,username):
        if (username in self.__groupDB):
            return self.__groupDB[username]
        return []
