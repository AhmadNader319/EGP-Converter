def _read_from_csv(csv_file_name):
    try:
        with open(csv_file_name, 'r') as csv_file:
            return csv_file.read()
    except FileNotFoundError:
        raise RuntimeError(f"CSV file not found: {csv_file_name}")
    except IOError as e:
        raise RuntimeError(f"Error reading CSV file {csv_file_name}: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while reading CSV: {e}")

def _load_list_to_csv(csv_file_name, data_to_load: list):
    try:
        with open(csv_file_name, 'a', newline='') as csv_file:
            for data in data_to_load[:]:
                if (data != '\n'):
                    csv_file.write(str(data))
                    csv_file.write('\n')
    except IOError as e:
        raise RuntimeError(f"Error writing list to CSV file {csv_file_name}: {e}")
    except TypeError as e:
        raise RuntimeError(f"Invalid data type in list for CSV write: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred while loading list to CSV: {e}")

def _load_dict_to_csv(csv_file_name, data_to_load: dict):
    try:
        with open(csv_file_name, 'a', newline='') as csv_file:
            for data in data_to_load.values():
                if (str(data) != "None"):
                    csv_file.write(str(data))
                    csv_file.write('\n')
    except IOError as e:
        raise RuntimeError("Error writing dict to CSV file")
    except AttributeError:
        raise RuntimeError("Input 'data_to_load' must be a dictionary.")
    except TypeError as e:
        raise RuntimeError("Invalid data type of dictionary")
    except Exception as e:
        raise RuntimeError("An unexpected error occurred")

def _load_list_of_dict_to_csv(csv_file_name, data_to_load: list):
    try:
        with open(csv_file_name, 'a', newline='') as csvfile:
            for row in data_to_load[:]:
                if (row != '\n'):
                    if not isinstance(row, dict):
                        raise TypeError("Expected dictionary in list")
                    for data in row.values():
                        if (str(data) != "None"):
                            csvfile.write(str(data))
                            csvfile.write('\n')
    except IOError as e:
        raise RuntimeError("Error writing list of dicts to CSV file")
    except TypeError as e:
        raise RuntimeError("Invalid data type in list of dicts")
    except AttributeError:
        raise RuntimeError("Elements in data_to_load must be dictionaries.")
    except Exception as e:
        raise RuntimeError("An unexpected error occurred")

def _load_dataframe_to_csv(csv_file_name ,dataframe):
    try:
        rates = dataframe.values.tolist()
        _load_list_to_csv(csv_file_name, rates)
    except AttributeError:
        raise RuntimeError(f"Input 'dataframe' must be a pandas DataFrame or similar object with .values.tolist().")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred")
