from ..etl import main_etl

def trigger_year_historical_etl(year: int):
    main_etl.run_historical_pipeline(year=year)


def trigger_month_historical_etl(year: int, month: int):
    main_etl.run_historical_pipeline(year=year, month=month)
