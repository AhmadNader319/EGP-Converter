import pandas as pd
import json
print("this is transform module")
def _split_string_into_lines(historical_data: str) -> list:
    """
    Breaks a long text into a list of shorter texts (lines).

    Imagine you have a long message with many sentences, each on a new line.
    This function takes that long message and gives you back a list where
    each item in the list is one of those sentences (one line).

    Args:
        historical_data (str): A long text that you want to split into separate lines.

    Returns:
        list: A list of text lines. Each item in the list is one line from the original text.

    Raises:
        TypeError: If the input is not text (a string) or if it's empty (None).
        RuntimeError: If something unexpected goes wrong while splitting the text.
    """
    try:
        # Check if the input is actually text (a string).
        # If it's not a string or if it's empty (None), it will stop and give an error.
        if not isinstance(historical_data, str):
            if historical_data is None:
                raise TypeError("Input cannot be empty (None).")
            else:
                raise TypeError("Input must be text (a string).")
        # This is the main part: it splits the text wherever there's a new line.
        return historical_data.splitlines()
    except Exception as e:
        # If any problem happens, it will tell you that it failed to split the text.
        raise RuntimeError(f"Failed to split string into lines: {e}") from e

def _parse_and_fix_json_string(unformatted_string: str) -> dict:
    """
    Reads a special kind of text (called JSON) and turns it into a Python dictionary.
    It also fixes small mistakes in the text so that Python can understand it.

    JSON is a way to store information, like a small data card.
    A Python dictionary is like a list of words and their meanings.

    Args:
        unformatted_string (str): A text that looks like JSON, but might have some small errors
                                  (like using single quotes instead of double quotes).

    Returns:
        dict: A Python dictionary that contains the information from the JSON text.

    Raises:
        ValueError: If the input text is empty (None) or if it's not proper JSON.
        TypeError: If the input is not text (a string).
        RuntimeError: If something unexpected goes wrong while reading the JSON text.
    """
    try:
        # Check if the input text is empty or not a string.
        if unformatted_string is None:
            raise ValueError("Input text cannot be empty (None).")
        if not isinstance(unformatted_string, str):
            raise TypeError("Input must be text (a string)")

        # Fix common mistakes: change single quotes to double quotes and "True" to "true".
        # JSON needs double quotes and "true" (small 't').
        formatted_string = unformatted_string.replace("\'", "\"").replace("True", "true")
        # This line reads the fixed JSON text and turns it into a Python dictionary.
        return json.loads(formatted_string)
    except json.JSONDecodeError as e:
        # This error means the text is not in a correct JSON format, even after fixing.
        raise ValueError(f"Invalid JSON format for string.") from e
    except Exception as e:
        # If any other problem happens, it tells you that it failed to read the JSON text.
        raise RuntimeError(f"An unexpected error occurred while parsing JSON string: {e}") from e

def _reformat_list_of_json_strings(unformatted_list_of_strings: list) -> list:
    """
    Takes a list of JSON texts and turns each one into a Python dictionary.
    It's like processing many data cards one by one.

    Args:
        unformatted_list_of_strings (list): A list where each item is a JSON text (string).

    Returns:
        list: A list of Python dictionaries. Each dictionary comes from one of the JSON texts.
              If a JSON text cannot be read, its place in the list will be empty (None).

    Raises:
        TypeError: If the input is not a list or if it's empty (None).
    """
    # Check if the input is a list.
    if not isinstance(unformatted_list_of_strings, list):
        if unformatted_list_of_strings is None:
            raise TypeError("Input must be a list, not empty (None).")
        else:
            raise TypeError("Input must be a list")

    json_data = [] # This will store the results (the dictionaries)
    # Go through each JSON text in the list.
    for i, string_data in enumerate(unformatted_list_of_strings):
        try:
            # Try to read and fix each JSON text using the function above.
            parsed_item = _parse_and_fix_json_string(string_data)
            json_data.append(parsed_item) # Add the dictionary to our list
        except (ValueError, TypeError) as e:
            # If a JSON text cannot be read, it prints a warning and adds an empty spot (None)
            # to the list so that the list still has the correct number of items.
            print(f"Warning: Failed to parse item, Details {e}")
            json_data.append(None)
    return json_data

def _load_json_into_df(json_data: list) -> pd.DataFrame:
    """
    Takes a list of Python dictionaries and puts them into a "DataFrame".
    A DataFrame is like a table with rows and columns, similar to a spreadsheet.

    Args:
        json_data (list): A list of Python dictionaries, where each dictionary represents one row of data.

    Returns:
        pd.DataFrame: A Pandas DataFrame (a table) containing the data from the dictionaries.

    Raises:
        TypeError: If the input is not a list or if it's empty (None).
        ValueError: If there's a problem turning the dictionaries into a DataFrame.
    """
    try:
        # Check if the input is a list.
        if not isinstance(json_data, list):
            if json_data is None:
                raise TypeError("Input cannot be empty (None).")
            else:
                raise TypeError("Input must be a list")
        # This line turns the list of dictionaries into a DataFrame (a table).
        return pd.DataFrame(json_data)
    except (ValueError, TypeError) as e:
        # If there's a problem, it means the dictionaries couldn't be correctly put into a table.
        raise ValueError("Failed to load JSON data into DataFrame.") from e

def _prepare_data_columns(historical_data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Selects only specific columns ('date', 'base', and 'rates') from a data table.

    Imagine you have a big spreadsheet with many columns (like Name, Age, City, Phone).
    This function helps you pick only the columns you need (like Name and City).

    Args:
        historical_data_frame (pd.DataFrame): The original data table (DataFrame) with many columns.

    Returns:
        pd.DataFrame: A new data table (DataFrame) that only has the 'date', 'base', and 'rates' columns.

    Raises:
        TypeError: If the input is not a DataFrame or if it's empty (None).
        IndexError: If the needed columns ('date', 'base', 'rates') are not found in the table.
        RuntimeError: If something unexpected goes wrong while picking the columns.
    """
    try:
        # Check if the input is actually a DataFrame (a table).
        if not isinstance(historical_data_frame, pd.DataFrame):
            if historical_data_frame is None:
                raise TypeError("Input cannot be empty (None).")
            else:
                raise TypeError("Input must be a Pandas DataFrame.")
        # This line picks only the columns named 'date', 'base', and 'rates'.
        return historical_data_frame[['date', 'base', 'rates']]
    except KeyError as e: # Changed IndexError to KeyError as missing columns are KeyError
        # This error happens if one of the needed columns ('date', 'base', or 'rates') is missing from the table.
        raise KeyError(f"One or more required columns ('date', 'base', 'rates') not found in the DataFrame: {e}.") from e
    except Exception as e:
        # If any other problem happens, it tells you that something went wrong while preparing the columns.
        raise RuntimeError(f"An unexpected error occurred during column preparation: {e}") from e
