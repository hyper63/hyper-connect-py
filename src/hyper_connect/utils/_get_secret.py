from typing import Union

from ramda import compose, head, is_empty, last, split
from typeguard import typechecked


@typechecked
def get_secret(network_location: str) -> Union[str, None]:

    secret: str = compose(head, split("@"), last, split(":"))(network_location)

    if is_empty(secret):
        return None
    else:
        return secret
