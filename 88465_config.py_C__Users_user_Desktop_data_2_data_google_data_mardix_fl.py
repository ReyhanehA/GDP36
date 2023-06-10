"""
Flask-MarcoPolo

config.py

This module contains config for different environment

Each class based on BaseConf is a different set of configuration for an active environment

For more config options: http://flask.pocoo.org/docs/0.10/config/

- How to use:

It's best to have a mechanism to differentiate dev from prod from staging etc

project_env = "Dev"

my_project = MarcoPolo.init(Flask(__name__), config="project_name.config.%s" % project_env)

"""


class BaseConf(object):
    """
    Base config
    """

    # Flask Default config: http://flask.pocoo.org/docs/0.10/config/
    DEBUG = True
    SECRET_KEY = None

    SERVER_NAME = None

    # Flask-Assets : http://flask-assets.readthedocs.org/
    ASSETS_DEBUG = False
    FLASK_ASSETS_USE_S3 = False
    FLASK_ASSETS_USE_CDN = False

    # Flask-Mail : http://pythonhosted.org/Flask-Mail/
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = None
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False


    # Flask-SQLAlchemy : http://pythonhosted.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_DATABASE_URI = None




class Prod(BaseConf):
    """ Production configuration """

    DEBUG = False


class Dev(BaseConf):
    """ Development configuration """

    DEBUG = True
    SECRET_KEY = "PLEASE_CHANGE_SECRET_KEY"


