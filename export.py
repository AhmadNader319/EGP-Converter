from utils import api_data_utils
from utils import db2_utils
from utils import csv_utils

def _extract_historical_month_data(year: int, month: int):
    """
    Gets historical currency exchange rates for a specific month.

    Args:
        year (int): The year you want to get data for (e.g., 2023).
        month (int): The month you want to get data for (from 1 for January to 12 for December).

    Returns:
        dict: A dictionary (like a collection of data) containing the currency rates for that month.

    Raises:
        TypeError: If 'year' or 'month' are not whole numbers.
        ValueError: If 'month' is not between 1 and 12.
        RuntimeError: If there's a problem connecting to the currency service
                      or if something else unexpected goes wrong.
    """
    # This line is mostly for checking and can be removed in the final code.
    # It prints the type of 'year' and 'month' to help during development.
    print(type(year), " : ", type(month))

    # Check if 'year' is a whole number. If not, stop and show an error.
    if not isinstance(year, int):
        raise TypeError("year should be a whole number (integer)")
    # Check if 'month' is a whole number. If not, stop and show an error.
    if not isinstance(month, int):
        raise TypeError("month should be a whole number (integer)")
    # Check if 'month' is a valid month (between 1 and 12). If not, stop and show an error.
    if (month < 1 or month > 12):
        raise ValueError("month should be in range 1-12")

    try:
        # This calls another tool (_fetch_currency_data_for_month) to get the actual data
        # from an online currency exchange service (API).
        return api_data_utils._fetch_currency_data_for_month(year, month)
    except (ConnectionError, TimeoutError):
        # If the script can't connect to the online service or if it takes too long,
        # it will stop and show an error message.
        raise RuntimeError("Failed to connect to the currency rates API")
    except Exception as e:
        # If any other unexpected problem happens, it will stop and show a general error.
        raise RuntimeError(f"An unexpected error occurred during data fetching. Details: {e}")


def _extract_historical_year_data(year):
    """
    Gets historical currency exchange rates for a whole year.

    Args:
        year (int): The year you want to get data for (e.g., 2022).

    Returns:
        dict: A dictionary containing the currency rates for that entire year.

    Raises:
        TypeError: If 'year' is not a whole number.
        RuntimeError: If there's a problem connecting to the currency service
                      or if something else unexpected goes wrong.
    """
    # Check if 'year' is a whole number. If not, stop and show an error.
    if not isinstance(year, int):
        raise TypeError("year should be a whole number (integer)")
    try:
        # This calls another tool (_fetch_currency_data_for_year) to get the data
        # from an online currency exchange service (API) for the entire year.
        return api_data_utils._fetch_currency_data_for_year(year)
    except (ConnectionError, TimeoutError):
        # If the script can't connect to the online service or if it takes too long,
        # it will stop and show an error message.
        raise RuntimeError("Failed to connect to the currency rates API")
    except Exception as e:
        # If any other unexpected problem happens, it will stop and show a general error.
        raise RuntimeError(f"An unexpected error occurred during data fetching. Details: {e}")

def _extract_historical_data_from_db(table_name = "historical_rates_2013_05"):
    """
    Gets historical currency exchange rates from a database table.

    Args:
        table_name (str, optional): The name of the table in the database
                                    where the historical data is stored.
                                    By default, it looks for "historical_rates_2013_05".

    Returns:
        list: A list of data from the specified database table.
              The exact format of the list depends on what the database tool returns.
    """
    # This calls a database tool (_get_historical_data_from_db) to read information
    # from a specific table in your database.
    return db2_utils._get_historical_data_from_db(table_name)

def _extract_latest_data():
    """
    Gets the most recent (latest) currency exchange rates.

    Returns:
        dict: A dictionary containing the very latest currency rates.

    Raises:
        RuntimeError: If there's a problem connecting to the currency service
                      or if something else unexpected goes wrong.
    """
    try:
        # This calls a tool (_get_api_latest_data) to get the most up-to-date
        # currency rates from an online service (API).
        return api_data_utils._get_api_latest_data()
    except (ConnectionError, TimeoutError):
        # If the script can't connect to the online service or if it takes too long,
        # it will stop and show an error message.
        raise RuntimeError("Failed to connect to the currency rates API")
    except Exception as e:
        # If any other unexpected problem happens, it will stop and show a general error.
        raise RuntimeError(f"An unexpected error occurred during data fetching. Details: {e}")

def _save_historical_data_into_csv(csv_file_name = "/Users/ahmednader/Desktop/Code Repository/EGP-Converter/historical.csv"):
    """
    Gets historical data from the database and saves it into a CSV file.

    A CSV file is a simple text file that can be opened in spreadsheet programs like Excel.

    Args:
        csv_file_name (str, optional): The full path and name of the CSV file
                                       where the data will be saved.
                                       By default, it saves to a specific path on Ahmed Nader's desktop.
    """
    # First, get the historical data from the database.
    historical_data = _extract_historical_data_from_db()
    # Then, use a CSV tool (_load_list_to_csv) to save this data into the specified CSV file.
    csv_utils._load_list_to_csv(csv_file_name, historical_data)

def _fetch_historical_data_from_csv(csv_file_name = "/Users/ahmednader/Desktop/Code Repository/EGP-Converter/historical.csv"):
    """
    Reads historical data from a CSV file.

    Args:
        csv_file_name (str, optional): The full path and name of the CSV file
                                       to read data from.
                                       By default, it reads from a specific path on Ahmed Nader's desktop.

    Returns:
        list: A list of data read from the CSV file.
              The exact format of the list depends on how the CSV tool reads the file.
    """
    # This calls a CSV tool (_read_from_csv) to read information from the specified CSV file.
    return csv_utils._read_from_csv(csv_file_name)
