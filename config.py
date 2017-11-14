# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:123456@localhost:5432/baocao?connect_timeout=5'
SQLALCHEMY_TRACK_MODIFICATIONS = False

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = False

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
WTF_CSRF_SECRET_KEY = 'secret'

UPLOAD_FOLDER = 'app/static/products'

##############
#### smtp ####
##############
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = True
MAIL_USERNAME = 'nguyentudb1995@gmail.com'
MAIL_PASSWORD = 'fwqrfqgqkilznrbs'
MAIL_DEFAULT_SENDER = 'GroceryStore <nguyentudb1995@gmail.com>'


#Wkhtmltopdf
WKHTMLTOPDF_BIN_PATH = 'F:\\Progrram Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
PDF_DIR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'pdf')