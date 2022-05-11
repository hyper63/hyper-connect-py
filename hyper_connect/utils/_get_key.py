from typing import Union

from ramda import compose, head, is_empty, last, split


# network_location example 1: "hyper app key:hyper app secret@cloud.hyper.io"
# network_location example 2: "api.github.com"
def get_key(network_location: str) -> Union[str, None]:
    key: str = compose(head, split(":"))(network_location)

    if is_empty(key):
        return None
    else:
        return key
