# --- Reformat date to American Date format
def _format_date_component(component: int):
    """
    Formats a number (like a month or day) to be always two digits.
    For example, if you give it '3', it gives back '03'. If you give it '12', it gives back '12'.

    This is useful for making dates look correct, especially in the American format
    where months and days often have two digits (e.g., 01/05/2023 instead of 1/5/2023).

    Args:
        component (int): A whole number representing a part of a date, like a day or a month.
                         It must be 1 or greater.

    Returns:
        str: The number as text (string), formatted to have two digits.
             If the number is less than 10, a '0' is added in front.

    Raises:
        ValueError: If the input number is 0 or less than 1 (negative).
                    Or if the input is not a whole number (integer).
    """
    # Check 1: If the number is exactly 0, that's not allowed for a date part.
    if (component == 0):
        raise ValueError("Date component cannot be zero. Must be 1 or greater.")
    # Check 2: If the number is less than 1 (meaning it's negative), that's also not allowed.
    if component < 1:
        raise ValueError(f"Date component cannot be negative or zero. Received: {component}.")
    try:
        # This is the main part that formats the number:
        # If the number is smaller than 10 (like 1, 2, ..., 9), it adds a "0" in front.
        # For example, 3 becomes "03".
        # If the number is 10 or more (like 10, 11, 12), it just turns it into text.
        # For example, 12 becomes "12".
        return f"0{component}" if component < 10 else str(component)
    except TypeError as e:
        # If the input was not a whole number (integer), this error tells you.
        raise ValueError(f"Input component must be an integer, got type {type(component).__name__}.") from e
