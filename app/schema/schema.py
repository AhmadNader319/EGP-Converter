from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class CurrencyRateResponse(BaseModel):
    RATE_ID: int
    RATE_DATE: date
    BASE_CURRENCY_CODE: str
    TARGET_CURRENCY_CODE: str
    EXCHANGE_RATE: Decimal

    class Config:
        orm_mode = True
