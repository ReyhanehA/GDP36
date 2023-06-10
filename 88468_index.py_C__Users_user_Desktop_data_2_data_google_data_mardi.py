"""
Flask-MarcoPolo

$project_name.views.index


"""

from flask import abort
from flask.ext.marcopolo import (MarcoPolo,
                                 route,
                                 flash_error,
                                 flash_success,
                                 flash_info,
                                 set_cookie,
                                 get_cookie)


class Index(MarcoPolo):
    route_base = "/"

    def index(self):
        return self.render()


class Example(MarcoPolo):
    """
    A example
    """

    def index(self):
        flash_success("This is a SUCCESS flash message")
        flash_info("This is an INFO flash message")
        flash_error("This is an ERROR flash message")
        return self.render()

    def text(self):
        return "Just render a normal text"

    def error_401(self):
        abort(401, "This is a 401 Error")

    def error_403(self):
        abort(403, "This is a 403 Error")

    def error_404(self):
        abort(404, "This is a 404 Error")

    def error_500(self):
        abort(500, "This is a 500 Error")

