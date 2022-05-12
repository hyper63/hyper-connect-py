import json
from typing import Any, Optional

from ramda import assoc, compose, default_to, dissoc, is_nil, reject

from hyper_connect.types import QueryOptions


def swap(old: str, cur: str):
    def associate(o):
        return assoc(cur, o[old], o)

    return compose(dissoc(old), associate)

    # fields: Optional[List[str]]
    # sort: Optional[List[Dict[str, SortOptions]]]
    # limit: Optional[int]
    # useIndex: Optional[str]


def to_data_query(selector: Any, options: Optional[QueryOptions]):

    compose_result: dict = compose(
        reject(is_nil),
        swap("useIndex", "use_index"),
        assoc("selector", selector),
        default_to({}),
    )(options)

    result: str = json.dumps(compose_result)

    return result
