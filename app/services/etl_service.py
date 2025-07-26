from ..etl import main_etl

def trigger_year_historical_etl(year: int):
    main_etl.run_historical_pipeline(year=year)

def trigger_month_historical_etl(year: int, month: int):
    print(f"DEBUG ETL Service: Calling main_etl with year={year} (type={type(year)}), month={month} (type={type(month)})")
    print(month)
    print(type(month))
    main_etl.run_historical_pipeline(year=year, month=month)
