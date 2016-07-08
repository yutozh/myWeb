import datetime
CSRF_ENABLED = True
SECRET_KEY = ''
SQLALCHEMY_DATABASE_URI = ""
SQLALCHEMY_TRACK_MODIFICATIONS = True

REMEMBER_COOKIE_DURATION = datetime.timedelta(7)
REMEMBER_COOKIE_HTTPONLY = True

basedir = ""
UPLOAD_FOLDER = basedir + '/static/user'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

POSTS_PER_PAGE = 4
POSTS_PER_PAGE_ADMIN = 8
POSTS_CHAT_PER_PAGE = 8
# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['']

# GeeTest
captcha_id = ""
private_key = ""