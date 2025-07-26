def _format_date_component(value: int) -> str:
    """
    Formats an integer date component (like month or day) into a two-digit string.
    e.g., 1 -> '01', 9 -> '09', 12 -> '12'.
    Raises ValueError if the input is not a positive integer.
    """
    if not isinstance(value, int) or value <= 0:
        # This is likely the exact check that's failing, or a similar one.
        # Ensure that the type is indeed an int and it's positive.
        raise ValueError(f"Date component must be a positive whole number (integer). Received: {value} (type: {type(value)})")
    return f"{value:02d}"

# You might have other utilities here, e.g.:
# def some_other_conversion_function(...):
#     pass
