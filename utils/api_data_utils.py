import requests
import time
from .config import (BASE_URL, ACCESS_KEY)
from .conversion_utils import _format_date_component

print(_format_date_component(5))

# --- Fetch current/latest data https://api.exchangeratesapi.io/v1/latest?access_key=API_KEY in real-time
def _get_api_latest_data():
    url = f"{BASE_URL}latest?access_key={ACCESS_KEY}"
    print(url)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("data fetched:", data)
        print("Latest Currency API Data Fetched Successfully!")
        return data
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error fetching currency data: {e} (Status Code: {e.response.status_code})")
        print("data fetched: None")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error fetching currency data: {e} (Network problem like DNS failure, refused connection, etc.)")
        print("data fetched: None")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error fetching currency data: {e} (The request timed out)")
        print("data fetched: None")
        return None
    except requests.exceptions.RequestException as e:
        print(f"General Request Error fetching currency data: {e} (Catch-all for other request issues)")
        print("data fetched: None")
        return None
    except ValueError as e:
        print(f"JSON Decoding Error: The API response could not be parsed as JSON: {e}")
        print("data fetched: None")
        return None
    except Exception as e:
        print(f"An unexpected error occurred in _get_api_latest_data: {e}")
        print("data fetched: None")
        return None
    finally:
        time.sleep(4)


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
        print("data fetched:", data)
        print("Currency API Data Fetched Successfully!")
        return data
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error fetching currency data for {year}-{formatted_month}-{formatted_day}: {e} (Status Code: {e.response.status_code})")
        print("data fetched: None")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error fetching currency data for {year}-{formatted_month}-{formatted_day}: {e} (Network problem)")
        print("data fetched: None")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error fetching currency data for {year}-{formatted_month}-{formatted_day}: {e} (The request timed out)")
        print("data fetched: None")
        return None
    except requests.exceptions.RequestException as e:
        print(f"General Request Error fetching currency data for {year}-{formatted_month}-{formatted_day}: {e}")
        print("data fetched: None")
        return None
    except ValueError as e: # This handles json.JSONDecodeError if response.json() fails
        print(f"JSON Decoding Error for {year}-{formatted_month}-{formatted_day}: The API response could not be parsed as JSON: {e}")
        print("data fetched: None")
        return None
    except Exception as e:
        print(f"An unexpected error occurred in _get_api_data_for_date for {year}-{formatted_month}-{formatted_day}: {e}")
        print("data fetched: None")
        return None
    finally:
        time.sleep(4) # This will execute whether an exception occurred or not

def _fetch_currency_data(year: int, month: int, day: int) -> dict:
    """
    Fetches currency data for a specific date.
    This function acts as a wrapper around _get_api_data_for_date.
    Its error handling relies on the wrapped function.
    """
    return _get_api_data_for_date(year, month, day)

# --- Fetch currency data for a month
def _fetch_currency_data_for_month(year, month) -> dict:
    """
    Fetches currency data for each day of a given month.
    Handles potential None returns from _fetch_currency_data.
    """
    month_data = {}
    for day in range(1, 32): # Range up to 32 to cover all days 1-31. Calendar logic might be needed for actual days in month.
        data_for_day = _fetch_currency_data(year, month, day)
        if data_for_day is not None:
            month_data[day] = data_for_day
        else:
            print(f"Warning: Could not fetch data for {year}-{month}-{day}. Skipping this day.")
    return month_data

# --- Fetch currency data for a year (01-MM for a year)
def _fetch_currency_data_for_year(year) -> dict:
    """
    Fetches currency data for the first day of each month in a given year.
    Handles potential None returns from _fetch_currency_data.
    """
    year_data = {}
    for month in range(1, 13): # Range for all 12 months
        data_for_month = _fetch_currency_data(year, month, 1) # Fetching for the 1st day of each month
        if data_for_month is not None:
            year_data[month] = data_for_month
        else:
            print(f"Warning: Could not fetch data for {year}-{month}-01. Skipping this month.")
    return year_data

# --- Fetch currency data for a time series (30 consecutive days at most)
def _fetch_currency_data_for_time_series(year: int, month: int, start_day: int, end_day: int) -> dict:
    """
    Fetches currency data for a specified range of days within a month.
    Handles potential None returns from _fetch_currency_data.
    """
    time_series_data = {}
    if not (1 <= start_day <= 31 and 1 <= end_day <= 31 and start_day <= end_day):
        print(f"Error: Invalid start_day ({start_day}) or end_day ({end_day}) provided for time series.")
        return {}

    for day in range(start_day, end_day + 1):
        data_for_day = _fetch_currency_data(year, month, day)
        if data_for_day is not None:
            time_series_data[day] = data_for_day
        else:
            print(f"Warning: Could not fetch data for {year}-{month}-{day} in time series. Skipping this day.")
    return time_series_data
