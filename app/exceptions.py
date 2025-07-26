class ExchangeRateNotFoundError(Exception):
    """Custom exception raised when exchange rate is not found in the database."""
    def __init__(self, message="Exchange rate not found for the specified date or currency."):
        self.message = message
        super().__init__(self.message)
