import pandas as pd
from export import _extract_historical_year_data, _extract_historical_month_data
from transform import _prepare_data_columns, _load_json_into_df, _parse_and_fix_json_string
from utils import db2_utils

def _process_historical_data(historical_data_raw: dict) -> pd.DataFrame:
    """
    Processes raw historical data by parsing, loading into a DataFrame, and preparing columns.

    Args:
        historical_data_raw (dict): A dictionary containing raw historical data,
                                    where values are expected to be JSON-like strings.

    Returns:
        pd.DataFrame: A processed Pandas DataFrame containing historical currency rates,
                      or an empty DataFrame if processing fails at any stage.
    """
    historical_list_of_dicts = []
    # Iterate through the raw data and attempt to parse each item
    for hist_data_item in historical_data_raw.values():
        try:
            # Parse and fix potentially malformed JSON strings
            parsed_item = _parse_and_fix_json_string(str(hist_data_item))
            historical_list_of_dicts.append(parsed_item)
        except (ValueError, TypeError) as e:
            # Skip entries that cannot be parsed and log the error
            print(f"Skipping malformed data entry: {e}")
            continue

    # If no valid data is parsed, return an empty DataFrame
    if not historical_list_of_dicts:
        print("No valid data to process after parsing.")
        return pd.DataFrame()

    # Load the list of dictionaries into a Pandas DataFrame
    df = _load_json_into_df(historical_list_of_dicts)
    if df.empty:
        print("DataFrame is empty after loading JSON.")
        return pd.DataFrame()

    try:
        # Prepare and clean the DataFrame columns (e.g., convert data types, rename)
        rates_df = _prepare_data_columns(df)
        return rates_df
    except (ValueError, KeyError, RuntimeError) as e:
        # Handle errors during data preparation
        print(f"Error preparing data columns: {e}")
        return pd.DataFrame()

def run_data_pipeline():
    """
    Runs the main data pipeline for extracting, processing, and loading historical currency rates.

    The pipeline offers two extraction choices:
    1. Extract historical data for a full year.
    2. Extract historical data for a specific month.

    After extraction, the data is processed and then inserted into a Db2 database
    table named 'CURRENCY_RATES'.
    """
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

    # Process the extracted raw data
    rates_df = _process_historical_data(historical_data_raw)
    if rates_df.empty:
        print("No rates data to load into the database. Exiting.")
        return

    # Display the processed DataFrame
    print(rates_df)

    conn = None
    try:
        # Establish a connection to the Db2 database
        conn = db2_utils._connect_to_database()
        if conn:
            print("\nConnected to Db2. Inserting data...")
            # Iterate over each row in the processed DataFrame for insertion
            for index, row in rates_df.iterrows():
                rate_date = row['date']
                base_currency_code = row['base']
                target_currency_code_dict = row['rates'] # 'rates' column is expected to be a dictionary

                # Iterate through the target currencies and their exchange rates
                for target_code, exchange_rate in target_currency_code_dict.items():
                    try:
                        # Insert each currency rate record into the database
                        db2_utils._insert_to_db(
                            conn,
                            "CURRENCY_RATES", # Table name
                            ['rate_date', 'base_currency_code', 'target_currency_code', 'exchange_rate'], # Column names
                            [rate_date, base_currency_code, target_code, exchange_rate] # Values
                        )
                        print(f"Successfully inserted: Date={rate_date}, Base={base_currency_code}, Target={target_code}, Rate={exchange_rate}")
                    except Exception as e:
                        # Log errors for individual record insertions
                        print(f"Failed to insert record: {rate_date}, {base_currency_code}, {target_code}. Error: {e}")
            print("Data insertion process completed.")
        else:
            print("Could not establish a connection to the database. Skipping insertion.")
    except Exception as e:
        print(f"An error occurred during database connection or insertion: {e}")
    finally:
        # Ensure the database connection is closed
        if conn:
            db2_utils._close_connection(conn) # Assuming a _close_connection method exists in db2_utils

if __name__ == "__main__":
    run_data_pipeline()
