import os

from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = os.getenv("DATABASE_URL")

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER = os.getenv("MAIL_SERVER")
USE_CREDENTIALS = os.getenv("USE_CREDENTIALS")
START_TLS = os.getenv("START_TLS")
VALIDATE_CERTS = os.getenv("VALIDATE_CERTS")
MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS")
