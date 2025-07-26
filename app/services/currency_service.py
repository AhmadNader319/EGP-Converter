import ibm_db
from ..utils import db2_utils
from ..core.config import CURRENCY_RATES

class ExchangeRateNotFoundError(Exception):
    """Raised when an exchange rate is not found in the database."""
    pass

def get_exchange_rate(rate_date: str, target_currency_code: str) -> float:
    conn = None
    try:
        conn = db2_utils._connect_to_database()
        if not conn:
            raise Exception("Failed to connect to the database.")

        query = (
            f"SELECT EXCHANGE_RATE FROM {CURRENCY_RATES} "
            f"WHERE RATE_DATE = '{rate_date}' AND TARGET_CURRENCY_CODE = '{target_currency_code}'"
        )

        exchange_rate_data = db2_utils._run_sql_query(conn, query)

        if not exchange_rate_data:
            # This should be allowed to propagate to FastAPI
            raise ExchangeRateNotFoundError(
                f"No exchange rate found for date: {rate_date} and target currency: {target_currency_code}"
            )

        rate_value = float(exchange_rate_data[0]["EXCHANGE_RATE"])
        print(f"Retrieved exchange rate (EUR to {target_currency_code}): {rate_value}")
        return rate_value

    except ExchangeRateNotFoundError:
        raise  # Let it bubble up to be handled in FastAPI
    except Exception as e:
        raise Exception(f"An error occurred while fetching exchange rate from DB: {e}")
    finally:
        if conn:
            ibm_db.close(conn)


def get_all_historical_rates() -> list:
    """
    Retrieves all historical currency exchange rates from the database.
    Each rate includes its date, base currency, target currency, and exchange rate.
    """
    conn = None
    try:
        conn = db2_utils._connect_to_database()
        if not conn:
            raise Exception("Failed to connect to the database.")

        # Use the _get_all_from_db utility from db2_utils
        rates = db2_utils._get_all_from_db(conn, CURRENCY_RATES)
        print(f"INFO: Successfully fetched {len(rates)} historical rates from {CURRENCY_RATES}.")
        return rates
    # Removed the specific 'except ibm_db.DB2Error as e:'
    except Exception as e:
        # This will now catch any exception raised by ibm_db or other issues
        raise Exception(f"An error occurred while fetching all rates from DB: {e}")
    finally:
        if conn:
            ibm_db.close(conn)


def convert_eur_to_currency(amount: float, target_currency_code: str, rate_date: str) -> float:
    """
    Converts an amount from EUR to a target currency using historical rates.
    """
    exchange_rate = get_exchange_rate(rate_date, target_currency_code)
    return exchange_rate * amount

def convert_currency_to_eur(amount: float, base_currency_code: str, rate_date: str) -> float:
    """
    Converts an amount from a base currency to EUR using historical rates.
    """
    exchange_rate_eur_to_base = get_exchange_rate(rate_date, base_currency_code)

    if exchange_rate_eur_to_base == 0:
        raise ValueError(f"Exchange rate from EUR to {base_currency_code} is zero, cannot convert to EUR.")

    return (1 / exchange_rate_eur_to_base) * amount

def convert_between_non_eur_currencies(amount: float, base_currency_code: str, target_currency_code: str, rate_date: str) -> float:
    """
    Converts an amount between two non-EUR currencies using EUR as an intermediate.
    """
    if base_currency_code == 'EUR' or target_currency_code == 'EUR':
        raise ValueError("This function is for converting between non-EUR currencies. Use 'convert_eur_to_currency' or 'convert_currency_to_eur' instead.")

    # Get EUR to base_currency rate
    eur_to_base_rate = get_exchange_rate(rate_date, base_currency_code)

    # Get EUR to target_currency rate
    eur_to_target_rate = get_exchange_rate(rate_date, target_currency_code)

    if eur_to_base_rate == 0:
        raise ValueError(f"Exchange rate from EUR to {base_currency_code} is zero, cannot perform cross-conversion.")

    # formula: amount * (1 / eur_to_base_rate) * eur_to_target_rate
    return (amount / eur_to_base_rate) * eur_to_target_rate
