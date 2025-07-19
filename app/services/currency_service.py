from ..utils import db2_utils
from ..core.config import CURRENCY_RATES

class ExchangeRateNotFoundError(Exception):
    pass # to be modified later to run ETL for the rate_date doesn't exist

def _get_exchange_rate(rate_date: str, target_currency_code: str) -> float:
    """
    Retrieves the historical exchange rate from EUR to the target currency for a given date.

    Args:
        rate_date (str): The date for which to retrieve the exchange rate (YYYY-MM-DD).
        target_currency_code (str): The target currency code (e.g., 'USD', 'EGP').

    Returns:
        float: The exchange rate (EUR to target_currency_code).

    Raises:
        ExchangeRateNotFoundError: If no rate is found for the given date and currency.
        Exception: For other database or query execution errors.
    """
    conn = db2_utils._connect_to_database()
    query = f"SELECT EXCHANGE_RATE FROM {CURRENCY_RATES} WHERE RATE_DATE = '{rate_date}' AND TARGET_CURRENCY_CODE = '{target_currency_code}'"

    exchange_rate_data = db2_utils._run_sql_query(conn, query)

    if not exchange_rate_data:
        raise ExchangeRateNotFoundError(
            f"No exchange rate found for date: {rate_date} and target currency: {target_currency_code}"
        )

    rate_value = float(exchange_rate_data[0]["EXCHANGE_RATE"])
    print(f"Retrieved exchange rate (EUR to {target_currency_code}): {rate_value}")
    return rate_value

def convert_eur_to_currency(amount: float, target_currency_code: str, rate_date: str) -> float:
    """
    Converts an amount from EUR to a target currency using historical rates.

    Args:
        amount (float): The amount in EUR to convert.
        target_currency_code (str): The target currency code (e.g., 'USD', 'EGP').
        rate_date (str): The date for the historical rate (YYYY-MM-DD).

    Returns:
        float: The converted amount in the target currency.

    Raises:
        ExchangeRateNotFoundError: If the EUR to target_currency rate is not found.
    """
    exchange_rate = _get_exchange_rate(rate_date, target_currency_code)
    return exchange_rate * amount

def convert_currency_to_eur(amount: float, base_currency_code: str, rate_date: str) -> float:
    """
    Converts an amount from a base currency to EUR using historical rates.

    Args:
        amount (float): The amount in the base currency to convert.
        base_currency_code (str): The base currency code (e.g., 'USD', 'EGP').
        rate_date (str): The date for the historical rate (YYYY-MM-DD).

    Returns:
        float: The converted amount in EUR.

    Raises:
        ExchangeRateNotFoundError: If the EUR to base_currency rate is not found.
        ValueError: If the exchange rate is zero, preventing division by zero.
    """
    # _get_exchange_rate returns EUR to base_currency_code rate
    # To convert from base_currency_code to EUR, use 1 / (EUR_to_base_rate)
    exchange_rate_eur_to_base = _get_exchange_rate(rate_date, base_currency_code)

    if exchange_rate_eur_to_base == 0:
        raise ValueError(f"Exchange rate from EUR to {base_currency_code} is zero, cannot convert to EUR.")

    return (1 / exchange_rate_eur_to_base) * amount

def convert_between_non_eur_currencies(amount: float, base_currency_code: str, target_currency_code: str, rate_date: str) -> float:
    """
    Converts an amount between two non-EUR currencies using EUR as an intermediate.

    Args:
        amount (float): The amount in the base currency to convert.
        base_currency_code (str): The base currency code (not EUR).
        target_currency_code (str): The target currency code (not EUR).
        rate_date (str): The date for the historical rates (YYYY-MM-DD).

    Returns:
        float: The converted amount in the target currency.

    Raises:
        ExchangeRateNotFoundError: If required exchange rates (EUR to base/target) are not found.
        ValueError: If an intermediate exchange rate is zero, preventing division by zero.
    """
    if base_currency_code == 'EUR' or target_currency_code == 'EUR':
        raise ValueError("This function is for converting between non-EUR currencies. Use 'convert_eur_to_currency' or 'convert_currency_to_eur' instead.")

    # Get EUR to base_currency rate
    eur_to_base_rate = _get_exchange_rate(rate_date, base_currency_code)

    # Get EUR to target_currency rate
    eur_to_target_rate = _get_exchange_rate(rate_date, target_currency_code)

    if eur_to_base_rate == 0:
        raise ValueError(f"Exchange rate from EUR to {base_currency_code} is zero, cannot perform cross-conversion.")

    # formula: amount * (1 / eur_to_base_rate) * eur_to_target_rate
    return (amount / eur_to_base_rate) * eur_to_target_rate


if __name__ == "__main__":
    print('1')
    print(convert_eur_to_currency(500, 'EGP', '2018-02-01'))
    print('2')
    print(convert_currency_to_eur(500, 'EGP', '2018-02-01'))
    print('3')
    print(convert_between_non_eur_currencies(500, 'EGP', 'USD', '2018-02-01'))
