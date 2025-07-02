from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import json
import pandas as pd

from EGP_Converter import export
from EGP_Converter import transform
from EGP_Converter import load

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME', '/opt/airflow')
OUTPUT_CSV_PATH = os.path.join(AIRFLOW_HOME, 'data', 'latest_rates.csv')

def _extract_data_callable():
    year_to_extract = 2013
    print(f"Starting extraction of historical currency data for year {year_to_extract}...")
    try:
        latest_data = export._extract_historical_year_data(year_to_extract)
        print(f"Extraction complete for year {year_to_extract}.")
        return json.dumps(latest_data) if isinstance(latest_data, (dict, list)) else latest_data
    except Exception as e:
        print(f"Error during extraction: {e}")
        raise

def _transform_data_callable(ti):
    print("Starting data transformation...")
    raw_data_json = ti.xcom_pull(task_ids='extract_latest_data')

    if raw_data_json is None:
        raise ValueError("No raw data received from extraction task.")
    try:
        parsed_data = json.loads(raw_data_json)
    except json.JSONDecodeError:
        print("Raw data is not a JSON string, attempting direct string parsing.")
        parsed_data = raw_data_json

    if isinstance(parsed_data, str):
        processed_item = transform._parse_and_fix_json_string(parsed_data)
        data_for_df = [processed_item]
    elif isinstance(parsed_data, (dict, list)):
        data_for_df = parsed_data if isinstance(parsed_data, list) else [parsed_data]
    else:
        raise TypeError(f"Unexpected data type from extraction: {type(parsed_data)}")

    df = transform._load_json_into_df(data_for_df)
    prepared_df = transform._prepare_data_columns(df)

    print("Data transformation complete.")
    return prepared_df.to_json(orient='split')

def _load_data_callable(ti):
    print(f"Starting data loading to CSV: {OUTPUT_CSV_PATH}")
    transformed_df_json = ti.xcom_pull(task_ids='transform_data')

    if transformed_df_json is None:
        raise ValueError("No transformed data received from transformation task.")

    transformed_df = pd.read_json(transformed_df_json, orient='split')

    success = load._load_rates_to_csv(OUTPUT_CSV_PATH, transformed_df)

    if success:
        print(f"Data successfully loaded to {OUTPUT_CSV_PATH}")
    else:
        raise RuntimeError(f"Failed to load data to {OUTPUT_CSV_PATH}")

with DAG(
    dag_id='egp_converter_etl_pipeline',
    start_date=datetime.utcnow() - timedelta(days=1),
    schedule=None,
    catchup=False,
    tags=['egp_converter', 'etl', 'api', 'data_pipeline'],
    description='A full ETL pipeline for EGP currency exchange rates: Extract, Transform, Load to CSV.'
) as dag:
    # Task-1: Extract latest data
    extract_latest_data_task = PythonOperator(
        task_id='extract_latest_data',
        python_callable=_extract_data_callable,
    )

    # Task-2: Transform the extracted data
    transform_data_task = PythonOperator(
        task_id='transform_data',
        python_callable=_transform_data_callable,
    )

    # Task-3: Load the transformed data to CSV
    load_data_to_csv_task = PythonOperator(
        task_id='load_data_to_csv',
        python_callable=_load_data_callable,
    )

    #Task dependencies
    extract_latest_data_task >> transform_data_task >> load_data_to_csv_task
