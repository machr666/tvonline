"""
SecureXMLRPCServer.py - simple XML RPC server supporting SSL.
Based on this article: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81549
For windows users: http://webcleaner.sourceforge.net/pyOpenSSL-0.6.win32-py2.4.exe
Also special thanks to http://rzemieniecki.wordpress.com/2012/08/10/quick-solution-to-ssl-in-simplexmlrpcserver-python-2-6-and-2-7/
"""

# Configure below
LISTEN_HOST='127.0.0.1' # You should not use '' here, unless you have a real FQDN.
LISTEN_PORT=1443

KEYFILE = 'certs/tvonline.key'
CERTFILE = 'certs/tvonline.crt'
# Configure above

import SocketServer
import BaseHTTPServer
import SimpleXMLRPCServer
import fcntl, ssl, socket, os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/../.."
sys.path.insert(0,parentdir) 

from TVOnlineService import TVOnlineService

class SecureXMLRPCServer(BaseHTTPServer.HTTPServer,SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
    """
	Secure XML-RPC server.

	It it very similar to SimpleXMLRPCServer but it uses HTTPS for transporting XML data.
    """
    def __init__(self, server_address, HandlerClass, logRequests=True):
        self.logRequests = logRequests
        SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self)
        SocketServer.BaseServer.__init__(self, server_address, HandlerClass)
	self.socket = ssl.wrap_socket(socket.socket(), server_side=True,
				      certfile=CERTFILE,keyfile=KEYFILE,
				      ssl_version=ssl.PROTOCOL_SSLv23)
        self.server_bind()
        self.server_activate()

        # [Bug #1222790] If possible, set close-on-exec flag; if a
        # method spawns a subprocess, the subprocess shouldn't have
        # the listening socket open.
        if hasattr(fcntl, 'FD_CLOEXEC'):
            flags = fcntl.fcntl(self.fileno(), fcntl.F_GETFD)
            flags |= fcntl.FD_CLOEXEC
            fcntl.fcntl(self.fileno(), fcntl.F_SETFD, flags)

class SecureXMLRpcRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    """
	Secure XML-RPC request handler class.
	It it very similar to SimpleXMLRPCRequestHandler but it uses HTTPS for transporting XML data.
    """
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)
        
    def do_POST(self):
        try:
            # Unmarshal request an execute it
            data = self.rfile.read(int(self.headers["content-length"]))
            response = self.server._marshaled_dispatch(
                    data, getattr(self, '_dispatch', None)
                )
        except: # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)
            self.wfile.flush()

            # shut down the connection
	    self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
    
def server(HandlerClass=SecureXMLRpcRequestHandler,
	   ServerClass=SecureXMLRPCServer,
	   instance=TVOnlineService()):	

    server_address = (LISTEN_HOST, LISTEN_PORT) # (address, port)
    server = ServerClass(server_address, HandlerClass)
    server.register_instance(instance)    
    sa = server.socket.getsockname()
    print "Serving HTTPS on", sa[0], "port", sa[1]
    server.serve_forever()

if __name__ == '__main__':
    server()
