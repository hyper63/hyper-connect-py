from typing import Union

from ramda import compose, head, is_empty, split
from typeguard import typechecked


@typechecked
def get_key(network_location: str) -> Union[str, None]:
    key: str = compose(head, split(":"))(network_location)

    if is_empty(key):
        return None
    else:
        return key
