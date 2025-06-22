from export import _read_from_csv
import pandas as pd
import json

def _split_string_into_lines(historical_data) -> list:
    return historical_data.splitlines()

def _parse_and_fix_json_string(unformatted_string_data) -> dict:
        formatted_string = unformatted_string_data.replace("\'", "\"").replace("True", "true")
        return json.loads(formatted_string)

def _reformat_list_of_json_strings() -> list:
    json_data = []
    for string_data in unformatted_list_of_strings:
        json_data.append(_parse_and_fix_json_string(string_data))
    return json_data

def _load_json_into_df(json_data):
    return pd.DataFrame(json_data)

def _prepare_data_columns(historical_data_frame):
    return historical_data_frame.iloc[:,3:6]
