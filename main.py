import pandas as pd
from export import _fetch_historical_data_from_csv, _extract_historical_year_data, _extract_historical_month_data
from transform import _split_string_into_lines, _reformat_list_of_json_strings, _prepare_data_columns, _load_json_into_df, _parse_and_fix_json_string
from load import _load_rates_to_csv

# extract
print("Choose an extraction method:")
print("1. Extract historical data for a full year")
print("2. Extract historical data for a specific month")

choice = input("Enter your choice (1 or 2): ")

if choice == '1':
    year = int(input("Enter the year (e.g., 2015): "))
    historical_data = _extract_historical_year_data(year)
elif choice == '2':
    year = int(input("Enter the year (e.g., 2016): "))
    month = int(input("Enter the month (1-12, e.g., 4): "))
    historical_data = _extract_historical_month_data(year, month)
# transform
historical_list = []
for hist_data in historical_data.values():
    parsed_string = _parse_and_fix_json_string(str(hist_data))
    historical_list.append(parsed_string)
df = _load_json_into_df(historical_list)
rates = _prepare_data_columns(df)
# load
_load_rates_to_csv("/Users/ahmednader/Desktop/Code Repository/EGP-Converter/rates/rates.csv", rates)
rate_data = _fetch_historical_data_from_csv("/Users/ahmednader/Desktop/Code Repository/EGP-Converter/rates/rates.csv")
print(rate_data)
