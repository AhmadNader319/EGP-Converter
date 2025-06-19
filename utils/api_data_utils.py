import requests
import time
from .config import (BASE_URL, ACCESS_KEY)
# --- Reformat date to American Date format
def _format_date_component(component):
     return f"0{component}" if component < 10 else str(component)


# --- Fetch current/latest data https://api.exchangeratesapi.io/v1/latest?access_key=API_KEY in real-time
def _get_api_latest_data():
    url = f"{BASE_URL}latest?access_key={ACCESS_KEY}"
    print(url)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("data fetched:",data)
        print("Latest Currency API Data Fetched Successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching currency data: {e}")
        data = None
        print("data fetched: ", data)
    time.sleep(4)
    return data

# --- Fetch Historical data from the API ---
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

def _fetch_currency_data(year: int, month: int, day: int) -> dict:
    return _get_api_data_for_date(year, month, day)

# --- Fetch currency data for a month
def _fetch_currency_data_for_month(year, month) -> dict:
    month_data = {}
    for day in range(1,31):
        month_data[day] = _fetch_currency_data(year,month,day)
    return month_data

# --- Fetch currency data for a year (01-MM for a year)
def _fetch_currency_data_for_year(year) -> dict:
    year_data = {}
    for month in range(1,13):
        year_data[month] = _fetch_currency_data(year, month, 1)
    return year_data

# --- Fetch currency data for a time series (30 consecutive days at most)
def _fetch_currency_data_for_time_series(year: int, month: int, start_day: int, end_day: int) -> dict:
    time_series_data = {}
    for day in range(start_day, end_day + 1):
        time_series_data[day] = _fetch_currency_data(year,month,day)
    return time_series_data

