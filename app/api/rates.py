# app/api/rates.py
from fastapi import APIRouter, HTTPException, Depends, status, Query
from datetime import date as dt_date
from typing import Optional, List, Dict, Any

# Import the currency conversion functions and exception
from ..services.currency_service import (
    convert_eur_to_currency,
    convert_currency_to_eur,
    convert_between_non_eur_currencies,
    get_all_historical_rates,
    ExchangeRateNotFoundError
)

# Import the ETL trigger service
from ..services.etl_service import trigger_month_historical_etl

router = APIRouter()

def validate_date_format(date_str: str = Query(..., description="Date in YYYY-MM-DD.")) -> str:
    """Validates YYYY-MM-DD date format."""
    try:
        dt_date.fromisoformat(date_str)
        return date_str
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid date format. Use YYYY-MM-DD."
        )

@router.get("/convert")
async def convert_currency(
    amount: float = Query(..., gt=0, description="Amount to convert."),
    from_currency: str = Query(..., min_length=3, max_length=3, description="Source currency code."),
    to_currency: str = Query(..., min_length=3, max_length=3, description="Target currency code."),
    rate_date: str = Depends(validate_date_format),
    trigger_etl_on_missing: bool = Query(True, description="Trigger ETL if rate is missing.")
):
    """
    Performs currency conversion for a historical date.
    Supports EUR to X, X to EUR, and X to Y (non-EUR) conversions.
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency == to_currency:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Source and target currencies cannot be the same."
        )

    converted_amount = None
    try:
        if from_currency == 'EUR':
            converted_amount = convert_eur_to_currency(amount, to_currency, rate_date)
        elif to_currency == 'EUR':
            converted_amount = convert_currency_to_eur(amount, from_currency, rate_date)
        else:
            converted_amount = convert_between_non_eur_currencies(amount, from_currency, to_currency, rate_date)

    except ExchangeRateNotFoundError:
        print(f"INFO: Rate missing for {from_currency} to {to_currency} on {rate_date}. Attempting ETL...")
        if trigger_etl_on_missing:
            try:
                year, month, _ = map(int, rate_date.split('-'))
                trigger_month_historical_etl(year=year, month=month)

                if from_currency == 'EUR':
                    converted_amount = convert_eur_to_currency(amount, to_currency, rate_date)
                elif to_currency == 'EUR':
                    converted_amount = convert_currency_to_eur(amount, from_currency, rate_date)
                else:
                    converted_amount = convert_between_non_eur_currencies(amount, from_currency, to_currency, rate_date)

            except ExchangeRateNotFoundError:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Rate for {from_currency} to {to_currency} on {rate_date} still not found after ETL."
                )
            except Exception as etl_e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error during ETL or re-conversion: {etl_e}"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rate for {from_currency} to {to_currency} on {rate_date} not found. Consider triggering ETL."
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Conversion input error: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )

    return {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": amount,
        "rate_date": rate_date,
        "converted_amount": converted_amount
    }


@router.get(
    "/historical-rates",
    response_model=List[Dict[str, Any]],
    summary="List All Historical Exchange Rates",
    description="Retrieves all historical currency exchange rates currently stored in the database.",
    tags=["Currency Data"]
)
async def list_all_historical_rates_endpoint():
    """
    Retrieves and lists all historical currency exchange rates stored in the database.
    Each item in the list represents a record with details like date, base currency,
    target currency, and the exchange rate.
    """
    try:
        rates = get_all_historical_rates()
        if not rates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No historical rates found in the database."
            )
        return rates
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve historical rates: {e}"
        )
