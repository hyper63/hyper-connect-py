from typing import Union

from ramda import compose, head, is_empty, last, split


# network_location example 1: "hyper app key:hyper app secret@cloud.hyper.io"
# network_location example 2: "api.github.com"
def get_secret(network_location: str) -> Union[str, None]:

    secret: str = compose(head, split("@"), last, split(":"))(network_location)

    if is_empty(secret):
        return None
    else:
        return secret
