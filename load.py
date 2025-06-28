import pandas as pd
from utils import csv_utils

def _load_rates_to_csv(csv_file_name, dataframe):
    try:
        csv_utils._load_dataframe_to_csv(csv_file_name, dataframe)
        return True

    except AttributeError as e:
        print("Problem accessing csv_utils._load_dataframe_to_csv")
        return False
    except FileNotFoundError as e:
        print("Error: The specified file path '{csv_file_name}' was not found or accessible.")
        return False
    except TypeError as e:
        print("Error: Type mismatch when calling _load_dataframe_to_csv.")
        return False
