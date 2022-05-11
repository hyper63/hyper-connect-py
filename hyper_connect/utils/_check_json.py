import json


def check_json(body: str) -> bool:
    try:
        data_as_dict = json.loads(body)
        return True
    except json.JSONDecodeError:
        return False
