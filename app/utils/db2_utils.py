import ibm_db # This is a special tool to talk to IBM Db2 databases
from ..core.config import (DB2_NAME, DB2_HOSTNAME, DB2_PORT, PATH_TO_SSL, DB2_UID, DB2_PWD, CURRENCY_RATES)
import csv # A tool for working with CSV files (like simple spreadsheets)
import json # A tool for working with JSON data (a way to store information)
print(DB2_NAME)
def _connect_to_database():
    """
    Connects to the Db2 database.

    This function uses important details (like database name, address, username, password)
    that are kept secret in a 'config' file. It creates a special "connection string"
    that helps the computer find and link to the database securely using SSL.

    Returns:
        ibm_db.Connection: An active connection to the Db2 database.
                           If the connection fails, it might stop the program or give an error.
    """
    # This part builds a "secret message" (connection string) with all the details
    # needed to connect to the database. These details come from the 'config' file.
    conn_str = (
        f"DATABASE={DB2_NAME};"
        f"HOSTNAME={DB2_HOSTNAME};"
        f"PORT={DB2_PORT};"
        "SECURITY=SSL;" # This means the connection is secure (like using HTTPS for websites)
        f"SSLServerCertificate={PATH_TO_SSL};" # This is a special file to prove the database is real
        f"UID={DB2_UID};" # Your username for the database
        f"PWD={DB2_PWD}" # Your password for the database
    )
    # This line is for checking during development, it prints the connection string.
    print("connection string",conn_str)
    # This line actually tries to connect to the Db2 database using the connection string.
    conn = ibm_db.connect(conn_str, '', '')
    # This line is also for checking, it prints the connection object to confirm it worked.
    print(conn)
    return conn # Gives back the connection so other parts of the code can use it

def _insert_to_db(conn, table_name, column_names, data):
    """
    Adds new information (a row) into a specific table in the database.

    Imagine a table in your database with columns like 'Date', 'Currency', 'Rate'.
    This function takes new information for these columns and adds it as a new row.

    Args:
        conn (ibm_db.Connection): The active connection to the database (from `_connect_to_database`).
        table_name (str): The name of the table where you want to add the data (e.g., "CURRENCY_RATES").
        column_names (list): A list of column names in the table where you want to put data
                             (e.g., ['rate_date', 'base_currency_code', 'exchange_rate']).
        data (list): A list of the actual values you want to put into those columns
                     (e.g., ['2023-01-01', 'USD', 1.05]).
    """
    # Joins the column names with ", " to create a list like "col1, col2, col3"
    columns_str = ", ".join(column_names)
    # Creates question marks for each piece of data. This helps prevent problems (like SQL injection).
    # If you have 3 pieces of data, it will be "?, ?, ?"
    placeholders = ", ".join(["?"] * len(data))

    # Creates the SQL command to add data. It looks like:
    # INSERT INTO YourTableName (column1, column2) VALUES (?, ?)
    sql_insert = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    # Prepares the SQL command to be sent to the database.
    stmt = ibm_db.prepare(conn, sql_insert)

    # This line is for checking during development, it prints the data before inserting.
    print("Data before inserting: ", data)

    # This part connects each piece of your 'data' to a question mark in the SQL command.
    for i, value in enumerate(data):
        ibm_db.bind_param(stmt, i + 1, value)

    # Runs the prepared SQL command, actually adding the data to the database.
    ibm_db.execute(stmt)
    # Saves the changes to the database permanently.
    ibm_db.commit(conn)
    # Cleans up the statement after use.
    ibm_db.free_stmt(stmt)

def _get_all_from_db(conn, table_name):
    """
    Gets all the information (all rows and columns) from a specific table in the database.

    Args:
        conn (ibm_db.Connection): The active connection to the database.
        table_name (str): The name of the table from which you want to get data.

    Returns:
        list: A list where each item is a dictionary (like a small collection of data)
              representing one row from the database table.
    """
    # Creates the SQL command to get all data from the table. It looks like:
    # SELECT * FROM YourTableName
    sql_select = f"SELECT * FROM {table_name}"
    # Prepares the SQL command.
    stmt = ibm_db.prepare(conn, sql_select)
    # Runs the SQL command to get the data.
    ibm_db.execute(stmt)

    result = [] # This list will hold all the rows we get from the database.
    # Gets the first row of data as a dictionary.
    row = ibm_db.fetch_assoc(stmt)
    # Continues to get rows until there are no more.
    while row:
        result.append(row) # Adds the current row to our list.
        row = ibm_db.fetch_assoc(stmt) # Gets the next row.

    # Cleans up the statement after use.
    ibm_db.free_stmt(stmt)
    return result # Gives back the list of all rows.

def _run_sql_query(conn, sql_stmt):
    """
    Gets all the information (all rows and columns) from a specific table in the database.

    Args:
        conn (ibm_db.Connection): The active connection to the database.
        table_name (str): The name of the table from which you want to get data.

    Returns:
        list: A list where each item is a dictionary (like a small collection of data)
              representing one row from the database table.
    """
    # Prepares the SQL command.
    stmt = ibm_db.prepare(conn, sql_stmt)
    # Runs the SQL command to get the data.
    ibm_db.execute(stmt)

    result = [] # This list will hold all the rows we get from the database.
    # Gets the first row of data as a dictionary.
    row = ibm_db.fetch_assoc(stmt)
    # Continues to get rows until there are no more.
    while row:
        result.append(row) # Adds the current row to our list.
        row = ibm_db.fetch_assoc(stmt) # Gets the next row.

    # Cleans up the statement after use.
    ibm_db.free_stmt(stmt)
    return result # Gives back the list of all rows.


if __name__ == "__main__":
    conn = _connect_to_database()
    query = f"select exchange_rate from {CURRENCY_RATES} where rate_date = '2000-02-01' and TARGET_CURRENCY_CODE = 'USD'"
    exchange_rate = _run_sql_query(conn, query)
    print(f"exchange rate {exchange_rate}")
    print(float(exchange_rate[0]["EXCHANGE_RATE"]))
