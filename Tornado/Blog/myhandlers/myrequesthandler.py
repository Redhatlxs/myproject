from tornado.web import RequestHandler

from day04.util.mysession import MySession


class MyRequestHandler(RequestHandler):
    def __init__(self,application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.session = MySession(self)

