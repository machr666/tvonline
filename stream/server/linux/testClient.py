import xmlrpclib
server = xmlrpclib.Server('https://localhost:1443')
server2 = xmlrpclib.Server('https://localhost:1443')
print server.shutdown("TVOnlineRules")
print server2.curUploadRate("TVOnlineRules")

