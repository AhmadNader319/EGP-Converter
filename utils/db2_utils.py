import ibm_db
from .config import (DB2_NAME, DB2_HOSTNAME, DB2_PORT, PATH_TO_SSL, DB2_UID, DB2_PWD, CURRENCY_RATES)
import csv
import json

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
    print("connection string",conn_str)
    conn = ibm_db.connect(conn_str, '', '')
    print(conn)
    return conn

def _insert_to_db(conn, table_name, column_names, data):
    columns_str = ", ".join(column_names)
    placeholders = ", ".join(["?"] * len(data))

    sql_insert = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    stmt = ibm_db.prepare(conn, sql_insert)

    print("Data before inserting: ", data)

    for i, value in enumerate(data):
        ibm_db.bind_param(stmt, i + 1, value)

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
