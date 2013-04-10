import os.path
import socket
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop

# User authentication and rights management
from usermgmt.XMLUserMgmtDAO import XMLUserMgmtDAO
userDAO = XMLUserMgmtDAO('data')

# Server configuration
from stream.server.XMLServerDAO import XMLServerDAO
from stream.server.ServerManager import ServerManager
serverMgr = ServerManager(XMLServerDAO('data'))

# Stream configuration
from stream.Stream import Stream
from stream.XMLStreamDAO import XMLStreamDAO
from stream.StreamManager import StreamManager
streamMgr = StreamManager(XMLStreamDAO(serverMgr,'data'))

from tornado.options import define, options

class TVServer(tornado.web.Application):
    ''' Configure server '''
    def __init__(self):
        handlers = [
            (r"/", ReqHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/tv", TVHandler),
            (r"/stream", StreamHandler),
            (r"/server", ServerManagerHandler),
            (r"/(\w+)", ReqHandler),
        ]
        mainDir = os.path.dirname(__file__)
        f = open('cookiesecret.txt','r')
        cookie_secret = f.read()
        f.close()
        settings = dict(
            xsrf_cookies = True,
            cookie_secret = cookie_secret,
            login_url = "/login",
            template_path = os.path.join(mainDir, "templates/myStyle"),
            static_path = os.path.join(mainDir, "templates/myStyle/static")
        )
        tornado.web.Application.__init__(self, handlers, **settings)

#---------------------------------------------------------------
#               Utility classes and functions
#---------------------------------------------------------------
class PersonalisedRequestHandler(tornado.web.RequestHandler):
    ''' This class specifies how we store the user identity '''

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def delete_session_cookie(self):
        self.clear_cookie("user");

# Decorator that checks both whether user is authenticated and
# if they are authorised
def requireAuth(groups=[]):
    def _decorator(f):
        @tornado.web.authenticated
        def wrappedF(self,*args):
            if (groups == [] or 
               [userDAO.isMemberOfGroup(self.current_user,group)
                       for group in groups].count(True) > 0):
                f(self,*args)
                return
            self.render("../noauth.html")
        return wrappedF
    return _decorator

#---------------------------------------------------------------
#               Request Handlers
#---------------------------------------------------------------
class LoginHandler(PersonalisedRequestHandler):
    ''' Show the login page and handle authentication process '''

    def get(self):
        if not self.current_user:
            self.render("../login.html", failure=False)
            return
        self.redirect("/")

    def post(self):
        # Login failure
        if (not userDAO.isLoginValid(self.get_argument("username"),
                                     self.get_argument("password"))):
            self.render("../login.html", failure=True)
            return

        # Login success
        self.set_secure_cookie("user", self.get_argument("username"))
        self.redirect("/")

class LogoutHandler(PersonalisedRequestHandler):
    ''' End the user's current session '''

    def get(self):
        self.delete_session_cookie()
        self.redirect("/")

class TVHandler(PersonalisedRequestHandler):
    ''' Handle get/post requests for the tv video page '''

    @requireAuth()
    def get(self):
        self.render("../tv.html", 
                    streams=streamMgr.activeStreams,
                    curStream='',
                    curStreamAddress='/static/images/chooseStream.jpg') 

    @requireAuth()
    def post(self):
        streamName = self.get_argument(streamMgr.STREAM,'')
        addr = streamMgr.requestStream(streamName)
        if (addr == Stream.STATE.BUSY):
            addr = '/static/images/busyStream.jpg'
        elif (addr == Stream.STATE.DOWN):
            addr = '/static/images/chooseStream.jpg'

        self.render("../tv.html", 
                    streams=streamMgr.activeStreams,
                    curStream=streamName,
                    curStreamAddress=addr) 

class ServerManagerHandler(PersonalisedRequestHandler):
    ''' Handle get/post requests for the server configuration page '''

    @requireAuth(["admin"])
    def get(self):
        self.render("../server.html", 
                    SERVER=serverMgr.SERVER,
                    STATE=serverMgr.STATE,
                    infrastructure=serverMgr.infrastructure)

    @requireAuth(["admin"])
    def post(self):
        serverMgr.changeServerState(self.get_argument(serverMgr.SERVER),
                                    self.get_argument(serverMgr.STATE))
        self.render("../server.html", 
                    SERVER=serverMgr.SERVER,
                    STATE=serverMgr.STATE,
                    infrastructure=serverMgr.infrastructure)

class StreamHandler(PersonalisedRequestHandler):
    ''' Handle get/post requests for the stream configuration page '''

    @requireAuth(["admin"])
    def get(self):
        self.render("../stream.html", streams=streamMgr.streams)

    @requireAuth(["admin"])
    def post(self):
        streamMgr.configureStream(self.get_argument(streamMgr.STREAM),
                                  self.request.arguments)
        self.render("../stream.html", streams=streamMgr.streams)

class ReqHandler(PersonalisedRequestHandler):
    ''' Handle get/post requests for the TVOnline website '''

    @requireAuth()
    def get(self, page="home"):
        self.render("../" + page + ".html")

    def get_error_html(self, status_code, **kwargs):
        self.render("../error.html")

#---------------------------------------------------------------
#               Launch the server
#---------------------------------------------------------------
define("port", default=8001, help="Server port", type=int)
mainDir = os.path.dirname(__file__)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(TVServer(),
        ssl_options = {"certfile": os.path.join(mainDir, "certs/tvonline.crt"),
                      "keyfile": os.path.join(mainDir, "certs/tvonline.key")})
    #http_server.listen(options.port)
    http_server.bind(options.port,family=socket.AF_INET)
    http_server.start(0)
    tornado.ioloop.IOLoop.instance().start()
