def _read_from_csv(csv_file_name):
    """
    Reads all the text from a CSV file.

    A CSV file is a simple text file that stores data in a table format,
    like a simple spreadsheet.

    Args:
        csv_file_name (str): The name of the CSV file you want to read.
                             For example, "my_data.csv".

    Returns:
        str: All the text content read from the CSV file.

    Raises:
        RuntimeError: If the file is not found, or if there's a problem reading it,
                      or if any other unexpected error happens.
    """
    try:
        # Tries to open the file with the given name for reading ('r').
        # 'with open(...) as csv_file:' makes sure the file is properly closed afterwards.
        with open(csv_file_name, 'r') as csv_file:
            return csv_file.read() # Reads everything from the file and returns it as one long text.
    except FileNotFoundError:
        # If the computer cannot find the file, this error is shown.
        raise RuntimeError(f"CSV file not found: {csv_file_name}")
    except IOError as e:
        # If there's another problem with opening or reading the file (e.g., permissions), this error is shown.
        raise RuntimeError(f"Error reading CSV file {csv_file_name}: {e}")
    except Exception as e:
        # If any other unexpected problem happens, this general error is shown.
        raise RuntimeError(f"An unexpected error occurred while reading CSV: {e}")

def _load_list_to_csv(csv_file_name, data_to_load: list):
    """
    Adds (writes) each item from a list into a CSV file, putting each item on a new line.

    This function adds data to the end of the file if the file already exists.
    If the file does not exist, it creates a new one.

    Args:
        csv_file_name (str): The name of the CSV file where you want to add the data.
        data_to_load (list): A list of items (can be numbers, text, etc.) that you want to save.
                             Each item will be written on a new line in the CSV.

    Raises:
        RuntimeError: If there's a problem writing to the file, if the data types in the list are wrong,
                      or if any other unexpected error happens.
    """
    try:
        # Opens the file in 'append' mode ('a'), which means new data will be added to the end.
        # 'newline=' ensures that lines are written correctly across different operating systems.
        with open(csv_file_name, 'a', newline='') as csv_file:
            # Loops through each piece of data in the list.
            for data in data_to_load[:]: # [:] creates a copy of the list, good practice
                # Check if the data is not just a newline character.
                if (data != '\n'):
                    csv_file.write(str(data)) # Writes the data (converted to text) to the file.
                    csv_file.write('\n')      # Adds a new line after each piece of data.
    except IOError as e:
        # If there's a problem writing to the file, this error is shown.
        raise RuntimeError(f"Error writing list to CSV file {csv_file_name}: {e}")
    except TypeError as e:
        # If the items in the list cannot be converted to text properly, this error is shown.
        raise RuntimeError(f"Invalid data type in list for CSV write: {e}")
    except Exception as e:
        # If any other unexpected problem happens, this general error is shown.
        raise RuntimeError(f"An unexpected error occurred while loading list to CSV: {e}")

def _load_dict_to_csv(csv_file_name, data_to_load: dict):
    """
    Adds (writes) only the *values* from a dictionary into a CSV file, each on a new line.

    This function adds data to the end of the file if the file already exists.
    If the file does not exist, it creates a new one.

    Args:
        csv_file_name (str): The name of the CSV file where you want to add the data.
        data_to_load (dict): A dictionary from which you want to save the values.
                             Each value will be written on a new line in the CSV.

    Raises:
        RuntimeError: If there's a problem writing to the file, if the input is not a dictionary,
                      if data types are wrong, or if any other unexpected error happens.
    """
    try:
        # Opens the file in 'append' mode ('a').
        with open(csv_file_name, 'a', newline='') as csv_file:
            # Loops through only the *values* of the dictionary.
            for data in data_to_load.values():
                # Checks if the data, when converted to text, is not the word "None".
                if (str(data) != "None"):
                    csv_file.write(str(data)) # Writes the data (converted to text) to the file.
                    csv_file.write('\n')      # Adds a new line.
    except IOError as e:
        # If there's a problem writing to the file.
        raise RuntimeError("Error writing dict to CSV file")
    except AttributeError:
        # If 'data_to_load' is not a dictionary (so it doesn't have '.values()').
        raise RuntimeError("Input 'data_to_load' must be a dictionary.")
    except TypeError as e:
        # If dictionary values cannot be converted to text properly.
        raise RuntimeError("Invalid data type of dictionary")
    except Exception as e:
        # Any other unexpected problem.
        raise RuntimeError("An unexpected error occurred")

def _load_list_of_dict_to_csv(csv_file_name, data_to_load: list):
    """
    Adds (writes) the values from each dictionary within a list into a CSV file.
    Each value from each dictionary is written on a new line.

    This function adds data to the end of the file if the file already exists.
    If the file does not exist, it creates a new one.

    Args:
        csv_file_name (str): The name of the CSV file where you want to add the data.
        data_to_load (list): A list where each item is a dictionary.
                             Only the values from these dictionaries will be saved.

    Raises:
        RuntimeError: If there's a problem writing to the file, if items in the list are not dictionaries,
                      if data types are wrong, or if any other unexpected error happens.
    """
    try:
        # Opens the file in 'append' mode ('a').
        with open(csv_file_name, 'a', newline='') as csvfile:
            # Loops through each item (which should be a dictionary) in the list.
            for row in data_to_load[:]:
                # Checks if the item is not just a newline character.
                if (row != '\n'):
                    # Checks if the current item is actually a dictionary.
                    if not isinstance(row, dict):
                        raise TypeError("Expected dictionary in list")
                    # Loops through only the *values* of the current dictionary.
                    for data in row.values():
                        # Checks if the data, when converted to text, is not the word "None".
                        if (str(data) != "None"):
                            csvfile.write(str(data)) # Writes the data (converted to text).
                            csvfile.write('\n')      # Adds a new line.
    except IOError as e:
        # If there's a problem writing to the file.
        raise RuntimeError("Error writing list of dicts to CSV file")
    except TypeError as e:
        # If items in the list are not dictionaries, or if dictionary values have issues.
        raise RuntimeError("Invalid data type in list of dicts")
    except AttributeError:
        # If an item in the list is not a dictionary and doesn't have '.values()'.
        raise RuntimeError("Elements in data_to_load must be dictionaries.")
    except Exception as e:
        # Any other unexpected problem.
        raise RuntimeError("An unexpected error occurred")

def _load_dataframe_to_csv(csv_file_name, dataframe):
    """
    Converts a Pandas DataFrame (a table-like structure) into a list of lists
    and then saves it into a CSV file.

    Args:
        csv_file_name (str): The name of the CSV file where you want to add the data.
        dataframe: A Pandas DataFrame object (a table of data).

    Raises:
        RuntimeError: If the input is not a DataFrame, or if any other unexpected error happens.
    """
    try:
        # Converts the DataFrame into a list of lists. Each inner list is a row from the DataFrame.
        rates = dataframe.values.tolist()
        # Calls the `_load_list_to_csv` function to save this list of lists into the CSV file.
        _load_list_to_csv(csv_file_name, rates)
    except AttributeError:
        # If 'dataframe' is not a Pandas DataFrame (or similar) and doesn't have '.values.tolist()'.
        raise RuntimeError(f"Input 'dataframe' must be a pandas DataFrame or similar object with .values.tolist().")
    except Exception as e:
        # Any other unexpected problem.
        raise RuntimeError(f"An unexpected error occurred")
