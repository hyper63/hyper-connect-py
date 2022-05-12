import json
from typing import Dict


def check_json(body: Dict) -> bool:
    try:
        # data_as_dict = json.loads(body)
        return True
    except json.JSONDecodeError:
        return False
