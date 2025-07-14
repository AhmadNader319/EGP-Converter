import ibm_db
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='/Users/ahmednader/Desktop/Code Repository/EGP-Converter/.env')

DB2_NAME = os.getenv("DB2_NAME")
DB2_HOSTNAME = os.getenv("DB2_HOSTNAME")
DB2_PORT = os.getenv("DB2_PORT")
DB2_UID = os.getenv("DB2_UID")
DB2_PWD = os.getenv("DB2_PWD")
PATH_TO_SSL = os.getenv("PATH_TO_SSL")
ACCESS_KEY = os.getenv("ACCESS_KEY")
CURRENCY_RATES = os.getenv("CURRENCY_RATES")
BASE_URL = os.getenv("BASE_URL")
BACKUP_ACCESS_KEY = os.getenv("BACKUP_ACCESS_KEY")

