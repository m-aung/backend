from utilities.formatters import format_date_to_utc

def format_date_and_serialize(data: tuple, keys: list) -> dict:
    return format_date_to_utc(data, keys, 'created_at')
