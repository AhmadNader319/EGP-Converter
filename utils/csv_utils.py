def _read_from_csv(csv_file_name):
    with open(csv_file_name) as csv_file:
        return csvfile.read()
def _load_to_csv(csv_file_name, data_to_load: list):
    with open(csv_file_name, 'w', newline='') as csvfile:
            for row in data_to_load[:]:
                if (row != '\\n'):
                    for data in row.values():
                        if (data != "None"):
                            csvfile.write(data)
                            csvfile.write('\n')
