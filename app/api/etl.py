from fastapi import APIRouter, HTTPException, Path, status
from typing import Optional

# Import the ETL trigger functions from your service layer
from ..services.etl_service import trigger_year_historical_etl, trigger_month_historical_etl

router = APIRouter()

@router.post("/trigger/historical/year/{year}")
async def trigger_historical_year_etl(
    year: int = Path(..., ge=2000, le=2100, description="Year to trigger ETL for (e.g., 2024).")
):
    """
    Triggers the historical ETL pipeline to fetch and load data for an entire year.
    """
    try:
        trigger_year_historical_etl(year=year)
        return {
            "message": f"Historical ETL pipeline triggered for year: {year}",
            "status": "triggered"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger historical year ETL for {year}: {e}"
        )

@router.post("/trigger/historical/month/{year}/{month}")
async def trigger_historical_month_etl(
    year: int = Path(..., ge=2000, le=2100, description="Year for ETL (e.g., 2024)."),
    month: int = Path(..., ge=1, le=12, description="Month for ETL (1-12, e.g., 7 for July).")
):
    """
    Triggers the historical ETL pipeline to fetch and load data for a specific month within a year.
    """
    print("hi hi hi hi hi hi")
    try:
        trigger_month_historical_etl(year=year, month=month)
        print(type(month))
        return {
            "message": f"Historical ETL pipeline triggered for {year}-{month:02d}",
            "status": "triggered"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger historical month ETL for {year}-{month}: {e}"
        )
