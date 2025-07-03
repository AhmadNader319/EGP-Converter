# --- Reformat date to American Date format
def _format_date_component(component: int):
    if (component == 0):
        raise ValueError("Date component cannot be zero. Must be 1 or greater.")
    if component < 1:
        raise ValueError(f"Date component cannot be negative or zero. Received: {component}.")
    try:
        return f"0{component}" if component < 10 else str(component)
    except TypeError as e:
        raise ValueError(f"Input component must be an integer, got type {type(component).__name__}.") from e # Value error for user-friendly Explanation
