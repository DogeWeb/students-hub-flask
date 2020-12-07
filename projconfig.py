import os

import os

basedir = os.path.abspath(os.path.dirname(__name__))


class BaseConfig(object):
    """Base configuration."""

    # main config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
    SECRET_KEY = '\x86\xc8\x9a\xd98\x01x\xb8\xd7B!\xac\x91\xcf\xa1\xc0\x845\xf7\xd1@\x9f]\xea'
    SECURITY_PASSWORD_SALT = 'Eo\x94\x86\x80G~!&\xba\xc1\xf9\xbd`\xfa\x1d\xcb\x8a\x02|\xbf\x88F\x89'
    UPLOAD_FOLDER = '/uploads'
    ALLOWED_EXTENSIONS = {'pdf'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    DEBUG = True
    # BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = 'students.hub.isproject@gmail.com'

    STYLE_TESTING = True
