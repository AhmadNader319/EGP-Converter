from utils import api_data_utils
from utils import db2_utils

def _extract_historical_month_data():
    return api_data_utils._fetch_currency_data_for_month(year, month)

def _extract_historical_data_from_db(table_name = "historical_rates_2013_05"):
    return db2_utils._get_historical_data_from_db(table_name)

def _extract_latest_data():
    return api_data_utils._get_api_latest_data()

def _extract_last_ten_data():
    return None

def _save_historical_data_into_csv(csv_file_name):
    with open(csv_file_name, 'w', newline='') as csvfile:
            for row in _extract_historical_data_from_db()[:]:
                if (row != '\\n'):
                    for data in row.values():
                        if (data != "None"):
                            csvfile.write(data)
                            csvfile.write('\n')

