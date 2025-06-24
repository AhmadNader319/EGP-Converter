def _read_from_csv(csv_file_name):
    with open(csv_file_name) as csv_file:
        return csv_file.read()
def _load_list_to_csv(csv_file_name, data_to_load: list):
    with open(csv_file_name, 'a', newline='') as csv_file:
            for data in data_to_load[:]:
                if (data != '\\n'):
                    print(str(data))
                    csv_file.write(str(data))
                    csv_file.write('\n')

def _load_dict_to_csv(csv_file_name, data_to_load: dict):
    with open(csv_file_name, 'a', newline='') as csv_file:
        for data in row.values():
            if (data != "None"):
                csv_file.write(str(data))
                csv_file.write('\n')

def _load_list_of_dict_to_csv(csv_file_name, data_to_load: list):
    with open(csv_file_name, 'a', newline='') as csvfile:
            for row in data_to_load[:]:
                if (row != '\\n'):
                    for data in row.values():
                        if (data != "None"):
                            csvfile.write(data)
                            csvfile.write('\n')

def _load_dataframe_to_csv(csv_file_name ,dataframe):
    rates = dataframe.values.tolist()
    _load_list_to_csv(csv_file_name, rates)
