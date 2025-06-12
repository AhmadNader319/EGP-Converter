import requests
import ibm_db
import time
from config import (_connect_to_database, DB2_HISTORICAL_TABLE_1, BASE_URL, ACCESS_KEY)

# --- Reformat date to American Date format
def _format_date_component(component):
     return f"0{component}" if component < 10 else str(component)

# --- Fetch currency data for a from the API ---
def _get_api_data_for_date(year, month, day):
    formatted_month = _format_date_component(month)
    formatted_day = _format_date_component(day)
    url = f"{BASE_URL}{year}-{formatted_month}-{formatted_day}?access_key={ACCESS_KEY}&symbols=EGP,USD,EUR,DZD&format=1"
    print(url)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("data fetched:",data)
        print("Currency API Data Fetched Successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching currency data: {e}")
        data = None
        print("data fetched: ", data)
    time.sleep(4)
    return data

def fetch_currency_data(year: int, month: int, day: int) -> dict:
    return _get_api_data_for_date(year, month, day)

def fetch_currency_data_for_month(year, month) -> dict:
    month_data = {}
    for day in range(1,31):
        month_data[day] = _get_api_data_for_date(year,day,month)
    return month_data

def fetch_currency_data_for_year(year) -> dict:
    year_data = {}
    for month in range(1,3):
        year_data[month] = _get_api_data_for_date(year, month, 1)
    return year_data

def insert_to_db(conn, table_name, data):
    sql_insert = f"INSERT INTO {table_name} (DAY_RATE) VALUES (?)"
    stmt = ibm_db.prepare(conn, sql_insert)

    full_api_response_string = str(data)
    print("data before inserting: ", data)
    ibm_db.bind_param(stmt, 1, full_api_response_string)
    ibm_db.execute(stmt)

    ibm_db.commit(conn)

    ibm_db.free_stmt(stmt)


def main():
    print("welcome to EGY currency convertor")
    conn = _connect_to_database()
    print("connection created")
    year_data = fetch_currency_data_for_year(2019)
    print("year data", year_data)
    print("start inserting into db")
    for month_rate in year_data.values():
        insert_to_db(conn, DB2_HISTORICAL_DATE_1, month_rate)


if __name__ == "__main__":
    main()
