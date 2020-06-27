import os

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'hms.db')
    JWT_SECRET_KEY = 'super-secret'
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'd1d7896e04afbd'
    MAIL_PASSWORD = '1db62f0e68b6a1'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False