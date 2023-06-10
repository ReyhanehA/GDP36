"""
Flask-MarcoPolo

$project_name.views.error

Error views for your application

In your other views, error pages can be invoked by using abort(404, message)
"""

from flask.ext.marcopolo import MarcoPolo


class Error(MarcoPolo):
    """
    Error Views
    """
    @classmethod
    def register(cls, app, **kwargs):
        super(cls, cls).register(app, **kwargs)

        # Bind the error to app
        @app.errorhandler(400)
        def error_400(error):
            return cls.error_400(error)

        # Bind the error to app
        @app.errorhandler(401)
        def error_401(error):
            return cls.error_401(error)

        @app.errorhandler(403)
        def error_403(error):
            return cls.error_403(error)

        @app.errorhandler(404)
        def error_404(error):
            return cls.error_404(error)

        @app.errorhandler(500)
        def error_500(error):
            return cls.error_500(error)

        @app.errorhandler(503)
        def error_503(error):
            return cls.error_503(error)

    @classmethod
    def error_400(cls, e):
        return cls.render(data={"error": e}), 400

    @classmethod
    def error_401(cls, e):
        return cls.render(data={"error": e}), 401

    @classmethod
    def error_403(cls, e):
        return cls.render(data={"error": e}), 403

    @classmethod
    def error_404(cls, e):
        return cls.render(data={"error": e}), 404

    @classmethod
    def error_500(cls, e):
        return cls.render(data={"error": e}), 500

    @classmethod
    def error_503(cls, e):
        return cls.render(data={"error": e}), 503