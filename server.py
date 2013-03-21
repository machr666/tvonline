import os.path
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop

from tornado.options import define, options
define("port", default=8080, help="Server port", type=int)

class TVServer(tornado.web.Application):
    ''' Configure server '''
    def __init__(self):
        handlers = [
            (r"/", ReqHandler),
            (r"/([a-zA-Z0-9-_]*\.html)", ReqHandler),
        ]
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates/myStyle"),
            static_path = os.path.join(os.path.dirname(__file__), "templates/myStyle/static"),
            debug = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class ReqHandler(tornado.web.RequestHandler):
    ''' Handle get requests '''
    def get(self, page="home.html"):
        print("Loading " + page)
        self.render("../"+page)

# Launch server
if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(TVServer())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
