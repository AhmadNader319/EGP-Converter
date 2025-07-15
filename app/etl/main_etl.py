import pandas as pd
from .export import _extract_historical_year_data, _extract_historical_month_data
from .transform import _prepare_data_columns, _load_json_into_df, _parse_and_fix_json_string
from ..utils import db2_utils

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

def run_historical_pipeline(year, month=None):
    """
    Runs the data pipeline to extract, process, and load historical currency rates
    for either a full year or a specific month if provided.

    Args:
        year (int): The year of historical data to extract.
        month (int, optional): The month (1-12). If None, extracts the full year.
    """
    historical_data_raw = None

    try:
        if month:
            historical_data_raw = _extract_historical_month_data(year, month)
            print(f"Extracted data for {year}-{month:02d}")
        else:
            historical_data_raw = _extract_historical_year_data(year)
            print(f"Extracted data for year {year}")
    except ValueError:
        print("Invalid year or month entered. Please enter numbers.")
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
                        print(f"Inserted: Date={rate_date}, Base={base_currency_code}, Target={target_code}, Rate={exchange_rate}")
                    except Exception as e:
                        if "SQL0803N" in str(e):
                            print(f"Duplicate record skipped: {rate_date}, {base_currency_code}, {target_code}")
                        else:
                            print(f"Failed to insert: {rate_date}, {base_currency_code}, {target_code}. Error: {e}")

            print("Data insertion completed.")
        else:
            print("Could not establish a database connection. Skipping insertion.")
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    run_historical_pipeline(2001)
