from ..utils import api_data_utils

# --- Fetch currency data for a month
def _get_currency_data_for_month(year, month) -> dict:
    return api_data_utils._fetch_currency_data_for_month(year, month)
# --- Fetch currency data for a year (01-MM for a year)
def _get_currency_data_for_year(year) -> dict:
    return api_data_utils._fetch_currency_data_for_year(year)
# --- Fetch currency data for a time series (30 consecutive days at most)
def _get_currency_data_for_time_series(year: int, month: int, start_day: int, end_day: int) -> dict:
    return api_data_utils._fetch_currency_data_for_time_series(year,month,start_day,end_day)
