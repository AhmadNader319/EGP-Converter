import ibm_db
from .config import (DB2_NAME, DB2_HOSTNAME, DB2_PORT, PATH_TO_SSL, DB2_UID, DB2_PWD, DB2_HISTORICAL_TABLE)
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

def _get_historical_data_from_db(table_name="historical_rates_2013_05"):
    try:
        conn = _connect_to_database()
        sql_select = f"SELECT * FROM {table_name}"
        print(f"Executing SQL: {sql_select}")
        stmt = ibm_db.prepare(conn, sql_select)
        ibm_db.execute(stmt)

        result = []
        row_count = 0
        row = ibm_db.fetch_assoc(stmt)
        while row:
            row_count += 1
            print(f"Fetched row {row_count}: {row}") # Print each row as it's fetched
            result.append(row)
            result.append('\\n')
            row = ibm_db.fetch_assoc(stmt)

        print(f"Total rows fetched: {row_count}")
        ibm_db.free_stmt(stmt)
        return result
    except TypeError as e:
        raise RuntimeError(f"Type error encountered: {e}") from e
    except AttributeError as e:
        raise RuntimeError(f"Attribute error encountered: {e}") from e
    except NameError as e:
        raise RuntimeError(f"Name error encountered: {e}") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}") from e
