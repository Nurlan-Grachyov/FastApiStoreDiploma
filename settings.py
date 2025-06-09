import os
from fastapi_mail import ConnectionConfig
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DATABASE_URL = os.getenv("DATABASE_URL")

MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
MAIL_FROM = os.getenv("MAIL_FROM"),
MAIL_PORT = os.getenv("MAIL_PORT"),
MAIL_SERVER = os.getenv("MAIL_SERVER"),
MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS"),
USE_CREDENTIALS = os.getenv("USE_CREDENTIALS"),
VALIDATE_CERTS = os.getenv("VALIDATE_CERTS"),
MAIL_STARTTLS = os.getenv("MAIL_STARTTLS")
