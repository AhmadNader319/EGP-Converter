import pandas as pd
import json

def _split_string_into_lines(historical_data: str) -> list:
    """Splits a multi-line string into a list of lines."""
    try:
        if not isinstance(historical_data, str):
            if historical_data is None:
                raise TypeError("Input cannot be None.")
            else:
                raise TypeError("Input must be a string.")
        return historical_data.splitlines()
    except Exception as e:
        raise RuntimeError(f"Failed to split string into lines: {e}") from e

def _parse_and_fix_json_string(unformatted_string: str) -> dict:
    """Parses and fixes a single JSON string."""
    try:
        if unformatted_string is None:
            raise ValueError("Input string cannot be None.")
        if not isinstance(unformatted_string, str):
            raise TypeError("Input must be a string")

        formatted_string = unformatted_string.replace("\'", "\"").replace("True", "true")
        return json.loads(formatted_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format for string.") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while parsing JSON string: {e}") from e

def _reformat_list_of_json_strings(unformatted_list_of_strings: list) -> list:
    """Parses and fixes a list of JSON strings."""
    if not isinstance(unformatted_list_of_strings, list):
        if unformatted_list_of_strings is None:
            raise TypeError("Input must be a list, not None.")
        else:
            raise TypeError("Input must be a list")

    json_data = []
    for i, string_data in enumerate(unformatted_list_of_strings):
        try:
            parsed_item = _parse_and_fix_json_string(string_data)
            json_data.append(parsed_item)
        except (ValueError, TypeError) as e:
            print(f"Warning: Failed to parse item, Details {e}")
            json_data.append(None)
    return json_data

def _load_json_into_df(json_data: list) -> pd.DataFrame:
    """Loads a list of JSON objects (dictionaries) into a Pandas DataFrame."""
    try:
        if not isinstance(json_data, list):
            if json_data is None:
                raise TypeError("Input cannot be None.")
            else:
                raise TypeError("Input must be a list")
        return pd.DataFrame(json_data)
    except (ValueError, TypeError) as e: # Pandas DataFrame constructor can raise these
        raise ValueError("Failed to load JSON data into DataFrame.") from e

def _prepare_data_columns(historical_data_frame: pd.DataFrame) -> pd.DataFrame:
    """Selects specific columns (3 to 5) from the DataFrame. {base, day, rates} columns"""
    try:
        if not isinstance(historical_data_frame, pd.DataFrame):
            if historical_data_frame is None:
                raise TypeError("Input cannot be None.")
            else:
                raise TypeError("Input must be a Pandas DataFrame.")
        return historical_data_frame[['date', 'base', 'rates']]
    except IndexError as e: # slice out of bounds
        raise IndexError(f"Column index out of bounds: {e}.") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during column preparation: {e}") from e
