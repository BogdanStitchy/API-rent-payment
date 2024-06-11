import os
from typing import Literal

from dotenv import load_dotenv

load_dotenv("config/.env")

MODE: Literal["DEV", "TEST", "PROD"] = os.environ['MODE']
LOG_LEVEL = os.environ['LOG_LEVEL']

DRIVER_DB = "asyncpg"
DIALECT_DB = "postgresql"

LOGIN_DB = os.environ['LOGIN_DB']
PASSWORD_DB = os.environ['PASSWORD_DB']
NAME_DB = os.environ['NAME_DB']
HOST = os.environ['HOST']
DB_PORT = os.environ['DB_PORT']
HASH_FUNCTION = os.environ['HASH_FUNCTION']
SECRET_KEY = os.environ['SECRET_KEY']

# TEST_LOGIN_DB = os.environ['TEST_LOGIN_DB']
# TEST_PASSWORD_DB = os.environ['TEST_PASSWORD_DB']
# TEST_NAME_DB = os.environ['TEST_NAME_DB']
# TEST_HOST = os.environ['TEST_HOST']
# TEST_PORT = os.environ['TEST_PORT']
#
# SMTP_HOST = os.environ['SMTP_HOST']
# SMTP_PORT = os.environ['SMTP_PORT']
# SMTP_USER = os.environ['SMTP_USER']
# SMTP_PASS = os.environ['SMTP_PASS']

HOST_REDIS = os.environ['HOST_REDIS']
SENTRY_DNS = os.environ['SENTRY_DNS']

DATABASE_URL = f"{DIALECT_DB}+{DRIVER_DB}://{LOGIN_DB}:{PASSWORD_DB}@{HOST}:{DB_PORT}/{NAME_DB}"
# TEST_DATABASE_URL = f"{DIALECT_DB}+{DRIVER_DB}://{TEST_LOGIN_DB}:{TEST_PASSWORD_DB}@{TEST_HOST}:{TEST_PORT}/{TEST_NAME_DB}"
