import pandas as pd
import json

def _split_string_into_lines(historical_data: str) -> list:
    return historical_data.splitlines()

def _parse_and_fix_json_string(unformatted_string: str) -> dict:
    formatted_string = unformatted_string.replace("\'", "\"").replace("True", "true")
    if (formatted_string != "None"):
        return json.loads(formatted_string)

def _reformat_list_of_json_strings(unformatted_list_of_strings: list) -> list:
    json_data = []
    for string_data in unformatted_list_of_strings:
        json_data.append(_parse_and_fix_json_string(string_data))
    return json_data

def _load_json_into_df(json_data: list):
    return pd.DataFrame(json_data)

def _prepare_data_columns(historical_data_frame):
    return historical_data_frame.iloc[:,3:6]
