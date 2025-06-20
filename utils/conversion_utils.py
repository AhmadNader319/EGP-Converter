# --- Reformat date to American Date format
def _format_date_component(component):
     return f"0{component}" if component < 10 else str(component)
