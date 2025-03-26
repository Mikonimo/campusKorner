import os
from dotenv import load_dotenv

load_dotenv()

# Must have a non-empty string for SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY', 'your-super-secret-key-here-for-development')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://mikonimo:8a3k5r13@localhost/campuskorner')
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 24))
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY', 'a434e1c37462db42be0c673358f0164d-us7')
MAILCHIMP_SERVER_PREFIX = os.getenv('MAILCHIMP_SERVER_PREFIX', 'us7')
MAILCHIMP_LIST_ID = os.getenv('MAILCHIMP_LIST_ID', '0714baed34')
