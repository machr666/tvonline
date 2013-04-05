from SocketServer import TCPServer

import ssl
import fcntl
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCDispatcher
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

from tvOnlineStreamServer import *

KEY_FILE = 'certs/tvonline.key'
CERT_FILE = 'certs/tvonline.crt'
PORT = 1443
ADDRESS = '127.0.0.1'

class SSLServer(TCPServer):
    def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        connstream = ssl.wrap_socket(newsocket, server_side=True,
                                     certfile=CERT_FILE, keyfile=KEY_FILE,
                                     ssl_version=ssl.PROTOCOL_SSLv23)
        return (connstream, fromaddr)

class SimpleXMLRPCServer(SSLServer, SimpleXMLRPCDispatcher):
    """ Simple secure XML-RPC server """
    allow_reuse_address = True

    # Warning: this is for debugging purposes only! Never set this to True in
    # production code, as will be sending out sensitive information (exception
    # and stack trace details) when exceptions are raised inside
    # SimpleXMLRPCRequestHandler.do_POST
    # _send_traceback_header = False

    def __init__(self, addr, requestHandler=SimpleXMLRPCRequestHandler,
                 logRequests=True, allow_none=False, encoding=None,
		 bind_and_activate=True):
        self.logRequests = logRequests

        SimpleXMLRPCDispatcher.__init__(self, allow_none, encoding)
        SSLServer.__init__(self, addr, requestHandler, bind_and_activate)

        # [Bug #1222790] If possible, set close-on-exec flag; if a
        # method spawns a subprocess, the subprocess shouldn't have
        # the listening socket open.
        if hasattr(fcntl, 'FD_CLOEXEC'):
            flags = fcntl.fcntl(self.fileno(), fcntl.F_GETFD)
            flags |= fcntl.FD_CLOEXEC
            fcntl.fcntl(self.fileno(), fcntl.F_SETFD, flags)

# Run the server
if __name__ == '__main__':
    print('Running XML-RPC server on port '+str(PORT))
    server = SimpleXMLRPCServer((ADDRESS, PORT))
    print('This server supports the following operations:')
    for fct in SERVER_FCTS:
        print(fct)
        server.register_function(globals()[fct])
    server.serve_forever()
