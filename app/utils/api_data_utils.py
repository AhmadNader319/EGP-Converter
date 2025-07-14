import requests # Used for making HTTP requests to web services (APIs)
import time     # Used for pausing the program (e.g., to avoid hitting API limits)
from .config import (BASE_URL, ACCESS_KEY) # Imports sensitive information (API base URL and access key) from a config file
from .conversion_utils import _format_date_component # Imports a helper function for formatting date parts

# This line is likely for testing the _format_date_component function when the script runs directly.
print(_format_date_component(5))

# --- Fetch current/latest data ---
def _get_api_latest_data() -> dict:
    """
    Fetches the most current (latest) currency exchange rates from the API.

    This function constructs a URL to get the very latest exchange rates
    and handles various network or API-related errors that might occur.

    Returns:
        dict: A Python dictionary containing the latest currency rate data if successful.
              Returns None if there's any error during the fetching process.
    """
    # Constructs the full URL for the 'latest' endpoint, including the API base URL and access key.
    url = f"{BASE_URL}latest?access_key={ACCESS_KEY}"
    print(url) # Prints the URL being accessed (useful for debugging).

    try:
        # Sends a GET request to the constructed URL.
        response = requests.get(url)
        # Checks if the HTTP request was successful (status code 200).
        # If not, it raises an HTTPError.
        response.raise_for_status()
        # Parses the JSON response body into a Python dictionary.
        data = response.json()
        print("data fetched:", data) # Prints the fetched data (for debugging/info).
        print("Latest Currency API Data Fetched Successfully!")
        return data # Returns the fetched data.

    except requests.exceptions.HTTPError as e:
        # Handles errors where the server responded with a 4xx (client error) or 5xx (server error) status code.
        print(f"HTTP Error fetching currency data: {e} (Status Code: {e.response.status_code})")
        print("data fetched: None")
        return None
    except requests.exceptions.ConnectionError as e:
        # Handles errors related to network problems (e.g., no internet, DNS issues, server not reachable).
        print(f"Connection Error fetching currency data: {e} (Network problem like DNS failure, refused connection, etc.)")
        print("data fetched: None")
        return None
    except requests.exceptions.Timeout as e:
        # Handles errors where the API server did not respond within a specified time limit.
        print(f"Timeout Error fetching currency data: {e} (The request timed out)")
        print("data fetched: None")
        return None
    except requests.exceptions.RequestException as e:
        # A general error handler for any other issues that might occur during the request.
        print(f"General Request Error fetching currency data: {e} (Catch-all for other request issues)")
        print("data fetched: None")
        return None
    except ValueError as e: # This specifically catches json.JSONDecodeError if response.json() fails
        # Handles errors where the API response is not valid JSON and cannot be parsed.
        print(f"JSON Decoding Error: The API response could not be parsed as JSON: {e}")
        print("data fetched: None")
        return None
    except Exception as e:
        # A catch-all for any other unexpected errors that were not specifically handled above.
        print(f"An unexpected error occurred in _get_api_latest_data: {e}")
        print("data fetched: None")
        return None
    finally:
        # This block always runs, whether an error occurred or not.
        # It pauses the program for 4 seconds to avoid hitting API rate limits.
        time.sleep(4)


# --- Fetch Historical data from the API for a specific date ---
def _get_api_data_for_date(year: int, month: int, day: int) -> dict:
    """
    Fetches historical currency exchange rates for a single, specific date.

    This function formats the given year, month, and day into a date string
    and constructs a URL to request historical data from the API. It includes
    error handling for various network and API response issues.

    Args:
        year (int): The year of the historical data (e.g., 2015).
        month (int): The month of the historical data (1-12, e.g., 4 for April).
        day (int): The day of the historical data (1-31).

    Returns:
        dict: A Python dictionary containing the historical currency rate data for the specified date.
              Returns None if there's any error during the fetching process.
    """
    # Formats the month and day to ensure they are always two digits (e.g., 5 becomes "05").
    formatted_month = _format_date_component(month)
    formatted_day = _format_date_component(day)
    # Constructs the full URL for the historical endpoint, including the date, API key,
    # and specific symbols (currencies) to fetch.
    url = f"{BASE_URL}{year}-{formatted_month}-{formatted_day}?access_key={ACCESS_KEY}&symbols=EGP,USD,EUR,DZD&format=1"
    print(url) # Prints the URL being accessed.

    try:
        # Sends a GET request to the historical data URL.
        response = requests.get(url)
        # Checks for HTTP errors (4xx or 5xx status codes).
        response.raise_for_status()
        # Parses the JSON response into a Python dictionary.
        data = response.json()
        print("data fetched:", data) # Prints the fetched data.
        print("Currency API Data Fetched Successfully!")
        return data # Returns the fetched data.

    except requests.exceptions.HTTPError as e:
        # Handles HTTP errors, providing specific context for the date.
        print(f"HTTP Error fetching currency data for {year}-{formatted_month}-{formatted_day}: {e} (Status Code: {e.response.status_code})")
        print("data fetched: None")
        return None
    except requests.exceptions.ConnectionError as e:
        # Handles network connection errors.
        print(f"Connection Error fetching currency data for {year}-{formatted_month}-{formatted_day}: {e} (Network problem)")
        print("data fetched: None")
        return None
    except requests.exceptions.Timeout as e:
        # Handles request timeouts.
        print(f"Timeout Error fetching currency data for {year}-{formatted_month}-{formatted_day}: {e} (The request timed out)")
        print("data fetched: None")
        return None
    except requests.exceptions.RequestException as e:
        # General error handler for other request issues.
        print(f"General Request Error fetching currency data for {year}-{formatted_month}-{formatted_day}: {e}")
        print("data fetched: None")
        return None
    except ValueError as e: # This handles json.JSONDecodeError if response.json() fails
        # Handles errors if the API response is not valid JSON.
        print(f"JSON Decoding Error for {year}-{formatted_month}-{formatted_day}: The API response could not be parsed as JSON: {e}")
        print("data fetched: None")
        return None
    except Exception as e:
        # Catch-all for any other unexpected errors.
        print(f"An unexpected error occurred in _get_api_data_for_date for {year}-{formatted_month}-{formatted_day}: {e}")
        print("data fetched: None")
        return None
    finally:
        # This block always runs. Pauses for 4 seconds to manage API request frequency.
        time.sleep(4)


def _fetch_currency_data(year: int, month: int, day: int) -> dict:
    """
    Fetches currency data for a specific date.

    This function acts as a straightforward wrapper, simply calling `_get_api_data_for_date`.
    Its error handling is managed by the wrapped function.

    Args:
        year (int): The year of the data.
        month (int): The month of the data.
        day (int): The day of the data.

    Returns:
        dict: The currency data for the specified date, or None if fetching fails.
    """
    return _get_api_data_for_date(year, month, day)

# --- Fetch currency data for a month ---
def _fetch_currency_data_for_month(year: int, month: int) -> dict:
    """
    Fetches currency data for each day of a given month.

    This function iterates through all possible days in a month (1 to 31,
    actual day count handled by the API itself or external validation)
    and attempts to fetch data for each day. It gracefully handles cases
    where data for a specific day cannot be fetched.

    Args:
        year (int): The year for which to fetch data.
        month (int): The month for which to fetch data (1-12).

    Returns:
        dict: A dictionary where keys are the day numbers (1-31) and values
              are the currency data dictionaries for that day. Days for which
              data could not be fetched will be absent from this dictionary.
    """
    month_data = {} # Initialize an empty dictionary to store data for the month
    # Loop from day 1 to day 31. The API will naturally return no data for invalid days (e.g., Feb 30).
    # A more robust solution might use the 'calendar' module to get exact days in a month.
    for day in range(1, 32):
        data_for_day = _fetch_currency_data(year, month, day)
        if data_for_day is not None:
            # If data was successfully fetched, add it to the month_data dictionary using the day as key.
            month_data[day] = data_for_day
        else:
            # If fetching failed for a day, print a warning and skip that day.
            print(f"Warning: Could not fetch data for {year}-{month}-{day}. Skipping this day.")
    return month_data

# --- Fetch currency data for a year (first day of each month) ---
def _fetch_currency_data_for_year(year: int) -> dict:
    """
    Fetches currency data for the first day of each month in a given year.

    This function is useful for getting a yearly overview by sampling the
    exchange rate on the first day of every month. It handles cases where
    data for a specific month's first day cannot be fetched.

    Args:
        year (int): The year for which to fetch data.

    Returns:
        dict: A dictionary where keys are the month numbers (1-12) and values
              are the currency data dictionaries for the first day of that month.
              Months for which data could not be fetched will be absent.
    """
    year_data = {} # Initialize an empty dictionary to store data for the year
    for month in range(1, 13): # Loop through all 12 months (1 to 12)
        # Fetch data specifically for the 1st day of the current month.
        data_for_month = _fetch_currency_data(year, month, 1)
        if data_for_month is not None:
            # If data was successfully fetched, add it to the year_data dictionary using the month as key.
            year_data[month] = data_for_month
        else:
            # If fetching failed for the 1st of a month, print a warning and skip that month.
            print(f"Warning: Could not fetch data for {year}-{month}-01. Skipping this month.")
    return year_data

# --- Fetch currency data for a time series (range of days) ---
def _fetch_currency_data_for_time_series(year: int, month: int, start_day: int, end_day: int) -> dict:
    """
    Fetches currency data for a specified range of days within a month.
    The API might have limitations (e.g., max 30 consecutive days).
    This function includes basic validation for the day range.

    Args:
        year (int): The year for the time series.
        month (int): The month for the time series.
        start_day (int): The starting day of the range (1-31).
        end_day (int): The ending day of the range (1-31). Must be >= start_day.

    Returns:
        dict: A dictionary where keys are the day numbers (from start_day to end_day)
              and values are the currency data dictionaries for that day.
              Days for which data could not be fetched will be absent.
    """
    time_series_data = {} # Initialize an empty dictionary for the time series data

    # Basic validation for the day range inputs.
    if not (1 <= start_day <= 31 and 1 <= end_day <= 31 and start_day <= end_day):
        print(f"Error: Invalid start_day ({start_day}) or end_day ({end_day}) provided for time series.")
        return {} # Return an empty dictionary if the range is invalid.

    # Loop through each day from the start_day to the end_day (inclusive).
    for day in range(start_day, end_day + 1):
        data_for_day = _fetch_currency_data(year, month, day)
        if data_for_day is not None:
            # If data was successfully fetched, add it to the time_series_data dictionary.
            time_series_data[day] = data_for_day
        else:
            # If fetching failed for a day, print a warning and skip it.
            print(f"Warning: Could not fetch data for {year}-{month}-{day} in time series. Skipping this day.")
    return time_series_data
