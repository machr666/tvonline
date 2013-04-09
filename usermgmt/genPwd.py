#!/usr/bin/python

import sys
from MockUserMgmtDAO import MockUserMgmtDAO

m = MockUserMgmtDAO()
print(m.hashPwd(sys.argv[1]))
