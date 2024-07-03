
from flask import Blueprint, redirect, url_for


class Routes():
    routes = []
    app = None

    def get(self, path, fn):
        self.app.add_url_rule(path, view_func=fn, methods=["GET"])
        pass

    def post(self, path, fn):
        self.app.add_url_rule(path, view_func=fn, methods=["POST"])
        pass

    def put(self, path, fn):
        self.app.add_url_rule(path, view_func=fn, methods=["PUT"])
        pass

    def patch(self, path, fn):
        self.app.add_url_rule(path, view_func=fn, methods=["PATCH"])
        pass

    def delete(self, path, fn):
        self.app.add_url_rule(path, view_func=fn, methods=["DELETE"])
        pass

    def redirect(self, path, to, method = "GET"):
        self.app.add_url_rule(path, view_func= lambda : redirect(url_for(to)), methods=[method])
        pass
    
    def middleware(self, fn):
        self.app.before_request(fn)
        pass

    def __init__(self, app=Blueprint) -> None:
        self.app = app
        pass
