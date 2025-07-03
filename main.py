import pandas as pd
from export import _extract_historical_year_data, _extract_historical_month_data
from transform import _prepare_data_columns, _load_json_into_df, _parse_and_fix_json_string
from utils import db2_utils

def _process_historical_data(historical_data_raw: dict) -> pd.DataFrame:
    historical_list_of_dicts = []
    for hist_data_item in historical_data_raw.values():
        try:
            parsed_item = _parse_and_fix_json_string(str(hist_data_item))
            historical_list_of_dicts.append(parsed_item)
        except (ValueError, TypeError) as e:
            print(f"Skipping malformed data entry: {e}")
            continue

    if not historical_list_of_dicts:
        print("No valid data to process after parsing.")
        return pd.DataFrame()

    df = _load_json_into_df(historical_list_of_dicts)
    if df.empty:
        print("DataFrame is empty after loading JSON.")
        return pd.DataFrame()

    try:
        rates_df = _prepare_data_columns(df)
        return rates_df
    except (ValueError, KeyError, RuntimeError) as e:
        print(f"Error preparing data columns: {e}")
        return pd.DataFrame()

def run_data_pipeline():
    print("Choose an extraction method:")
    print("1. Extract historical data for a full year")
    print("2. Extract historical data for a specific month")
    choice = input("Enter your choice (1 or 2): ")

    historical_data_raw = None
    if choice == '1':
        try:
            year = int(input("Enter the year (e.g., 2015): "))
            historical_data_raw = _extract_historical_year_data(year)
        except ValueError:
            print("Invalid year entered. Please enter a number.")
            return
    elif choice == '2':
        try:
            year = int(input("Enter the year (e.g., 2016): "))
            month = int(input("Enter the month (1-12, e.g., 4): "))
            historical_data_raw = _extract_historical_month_data(year, month)
        except ValueError:
            print("Invalid year or month entered. Please enter numbers.")
            return
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return

    if historical_data_raw is None:
        print("No historical data extracted. Exiting.")
        return

    rates_df = _process_historical_data(historical_data_raw)
    if rates_df.empty:
        print("No rates data to load into the database. Exiting.")
        return

    print(rates_df)

    conn = None
    try:
        conn = db2_utils._connect_to_database()
        if conn:
            print("\nConnected to Db2. Inserting data...")
            for index, row in rates_df.iterrows():
                rate_date = row['date']
                base_currency_code = row['base']
                target_currency_code_dict = row['rates']

                for target_code, exchange_rate in target_currency_code_dict.items():
                    try:
                        db2_utils._insert_to_db(
                            conn,
                            "CURRENCY_RATES",
                            ['rate_date', 'base_currency_code', 'target_currency_code', 'exchange_rate'],
                            [rate_date, base_currency_code, target_code, exchange_rate]
                        )
                        print("Successfully inserted")
                    except Exception as e:
                        print(f"Failed to insert record: {rate_date}, {base_currency_code}, {target_code}. Error: {e}")
            print("Data insertion process completed.")
        else:
            print("Could not establish a connection to the database. Skipping insertion.")
    except Exception as e:
        print(f"An error occurred during database connection or insertion: {e}")

if __name__ == "__main__":
    run_data_pipeline()
