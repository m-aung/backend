import datetime
from typing import List, Tuple, Dict, Any

def format_date_to_utc(data: Tuple[Any, ...], keys: List[str], dateKey: str) -> Dict[str, Any]:
    """Formats the data to a dictionary with the keys provided."""
    converted_dict = dict(zip(keys, data))
    if dateKey not in converted_dict:
        return converted_dict
    if converted_dict[dateKey] is not None:
        converted_dict[dateKey] = converted_dict[dateKey].astimezone(datetime.timezone.utc).isoformat()
    return converted_dict
