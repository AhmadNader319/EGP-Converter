import ibm_db
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB2_NAME = os.getenv("DB2_NAME")
DB2_HOSTNAME = os.getenv("DB2_HOSTNAME")
DB2_PORT = os.getenv("DB2_PORT")
DB2_UID = os.getenv("DB2_UID")
DB2_PWD = os.getenv("DB2_PWD")
PATH_TO_SSL = os.getenv("PATH_TO_SSL")
ACCESS_KEY = os.getenv("ACCESS_KEY")
DB2_HISTORICAL_TABLE_1 = os.getenv("DB2_HISTORICAL_TABLE_1")
BASE_URL = os.getenv("BASE_URL")
BACKUP_ACCESS_KEY = os.getenv("BACKUP_ACCESS_KEY")

def _connect_to_database():
    conn_str = (
        f"DATABASE={DB2_NAME};"
        f"HOSTNAME={DB2_HOSTNAME};"
        f"PORT={DB2_PORT};"
        "SECURITY=SSL;"
        f"SSLServerCertificate={PATH_TO_SSL};"
        f"UID={DB2_UID};"
        f"PWD={DB2_PWD}"
    )
    conn = ibm_db.connect(conn_str, '', '')
    return conn
