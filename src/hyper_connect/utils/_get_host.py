from typing import Union

from ramda import compose, is_empty, last, split
from typeguard import typechecked

# network_location example 1: "hyper app key:hyper app secret@cloud.hyper.io"
# network_location example 2: "api.github.com"


@typechecked
def get_host(network_location: str) -> Union[str, None]:

    host: str = compose(last, split("@"))(network_location)

    if is_empty(host):
        return None
    else:
        return host
