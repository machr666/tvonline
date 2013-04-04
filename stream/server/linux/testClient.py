import xmlrpclib
server = xmlrpclib.Server('https://localhost:1443')
print server.curUploadRate("TVOnlineRules")

