import pandas as pd
from ..utils import csv_utils

def _load_rates_to_csv(csv_file_name, dataframe):
    """
    Saves a table of currency rates into a CSV file.

    A CSV file is like a simple spreadsheet that you can open with programs
    like Excel. It's a good way to save data in a simple text format.

    Args:
        csv_file_name (str): The name of the CSV file where you want to save the data.
                             For example, "currency_rates.csv".
        dataframe (pd.DataFrame): This is the table (or "DataFrame") of currency rates
                                  that you want to save. It's like a spreadsheet in Python.

    Returns:
        bool: Returns True if the data was saved successfully to the CSV file.
              Returns False if there was a problem saving the data.
    """
    try:
        # This line uses a special tool (_load_dataframe_to_csv from csv_utils)
        # to write your 'dataframe' (the table of rates) into the 'csv_file_name'.
        csv_utils._load_dataframe_to_csv(csv_file_name, dataframe)
        return True # If it worked, say True

    except AttributeError as e:
        # This error happens if the script can't find the saving tool.
        # It means 'csv_utils' might be missing something important.
        print("Problem accessing csv_utils._load_dataframe_to_csv")
        return False
    except FileNotFoundError as e:
        # This error happens if the computer can't find the place to save the file,
        # or if it doesn't have permission to save there.
        print(f"Error: The specified file path '{csv_file_name}' was not found or accessible.")
        return False
    except TypeError as e:
        # This error happens if the 'csv_utils._load_dataframe_to_csv' tool
        # was given the wrong kind of information (e.g., something that is not a file name
        # or something that is not a dataframe).
        print("Error: Type mismatch when calling _load_dataframe_to_csv.")
        return False
