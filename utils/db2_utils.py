import ibm_db
from ..config import (DB2_NAME, DB2_HOSTNAME, DB2_PORT, PATH_TO_SSL, DB2_UID, DB2_PWD)

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

def _insert_to_db(conn, table_name, column_name, data):
    sql_insert = f"INSERT INTO {table_name} ({column_name}) VALUES (?)"
    stmt = ibm_db.prepare(conn, sql_insert)

    full_api_response_string = str(data)
    print("data before inserting: ", data)
    ibm_db.bind_param(stmt, 1, full_api_response_string)
    ibm_db.execute(stmt)

    ibm_db.commit(conn)

    ibm_db.free_stmt(stmt)

def _get_all_from_db(conn, table_name):
    sql_select = f"SELECT * FROM {table_name}"
    stmt = ibm_db.prepare(conn, sql_select)
    ibm_db.execute(stmt)

    result = []
    row = ibm_db.fetch_assoc(stmt)
    while row:
        result.append(row)
        row = ibm_db.fetch_assoc(stmt)

    ibm_db.free_stmt(stmt)
    return result
