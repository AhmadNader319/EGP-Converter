from utils import csv_utils
import pandas as pd

def _load_rates_to_csv(csv_file_name ,dataframe):
    csv_utils._load_dataframe_to_csv(csv_file_name, dataframe)
