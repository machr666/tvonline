import os.path

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop

# User authentication and rights management
from usermgmt.MockUserMgmtDAO import MockUserMgmtDAO
userDAO = MockUserMgmtDAO()

# Stream configuration
from stream.config.XMLConfigDAO import XMLConfigDAO
cfgDAO = XMLConfigDAO("data/")

## Stream control
#from stream.StreamControl import StreamControl
#from stream.MockProgramDAO import MockProgramDAO
#streamCtrl = StreamControl(MockProgramDAO(),"Not implemented yet")

# Server configuration
from stream.server.ServerManager import ServerManager
from stream.server.XMLServerDAO import XMLServerDAO
serverMgr = ServerManager(XMLServerDAO("data/"))

from tornado.options import define, options
define("port", default=8080, help="Server port", type=int)

class TVServer(tornado.web.Application):
    ''' Configure server '''
    def __init__(self):
        handlers = [
            (r"/", ReqHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/tv", TVHandler),
            (r"/config", ConfigHandler),
            (r"/server", ServerManagerHandler),
            (r"/(\w+)", ReqHandler),
        ]
        mainDir = os.path.dirname(__file__)
        settings = dict(
            xsrf_cookies = True,
            cookie_secret = "bls9+x7PT5GIbaBuKzsGOecL9SG7KUmEh6rNbMYTpfk=",
            login_url = "/login",
            template_path = os.path.join(mainDir, "templates/myStyle"),
            static_path = os.path.join(mainDir, "templates/myStyle/static"),
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
        self.render("../tv.html", stream=streamCtrl)

    @requireAuth()
    def post(self):
        self.render("../tv.html", stream=streamCtrl)

class ConfigHandler(PersonalisedRequestHandler):
    ''' Handle get/post requests for the stream configuration page '''

    @requireAuth(["config"])
    def get(self):
        self.render("../config.html", cfg=cfgDAO.loadConfig(), status="")

    @requireAuth(["config"])
    def post(self):
        ret = cfgDAO.persistConfig(self.get_argument("AudioCodec"),
                          self.get_argument("AudioRate"),
                          self.get_argument("VideoCodec"),
                          self.get_argument("VideoRate"),
                          self.get_argument("VideoSize"),
                          self.get_argument("StreamEncryption"))
        self.render("../config.html", cfg=cfgDAO.loadConfig(), status=ret[1])

class ServerManagerHandler(PersonalisedRequestHandler):
    ''' Handle get/post requests for the server configuration page '''

    @requireAuth(["config"])
    def get(self):
        self.render("../server.html", 
                    SERVER=serverMgr.SERVER,
                    STATE=serverMgr.STATE,
                    infrastructure=serverMgr.infrastructure)

    @requireAuth(["config"])
    def post(self):
        serverMgr.changeServerState(self.get_argument(serverMgr.SERVER),
                                    self.get_argument(serverMgr.STATE))
        self.render("../server.html", 
                    SERVER=serverMgr.SERVER,
                    STATE=serverMgr.STATE,
                    infrastructure=serverMgr.infrastructure)

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
if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(TVServer())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
