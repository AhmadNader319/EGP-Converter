from utils import api_data_utils
from utils import db2_utils
from utils import csv_utils

def _extract_historical_month_data(year, month):
    return api_data_utils._fetch_currency_data_for_month(year, month)

def _extract_historical_year_data(year):
    return api_data_utils._fetch_currency_data_for_year(year)

def _extract_historical_data_from_db(table_name = "historical_rates_2013_05"):
    return db2_utils._get_historical_data_from_db(table_name)

def _extract_latest_data():
    return api_data_utils._get_api_latest_data()

def _save_historical_data_into_csv(csv_file_name = "/Users/ahmednader/Desktop/Code Repository/EGP-Converter/historical.csv"):
    historical_data = _extract_historical_data_from_db()
    csv_utils._load_list_to_csv(csv_file_name, historical_data)

def _fetch_historical_data_from_csv(csv_file_name = "/Users/ahmednader/Desktop/Code Repository/EGP-Converter/historical.csv"):
    return csv_utils._read_from_csv(csv_file_name)

