import json
from typing import Dict, Optional

import requests
from promisio import promisify
from ramda import assoc

from hyper_connect.types import HyperRequest, HyperRequestParams
from hyper_connect.utils import create_hyper_request_params


@promisify
def add_cache(
    key: str,
    value: Dict,
    ttl: Optional[str],
    connection_string: str,
    domain: str = "default",
):
    cache_doc = {"key": key, "value": value}

    if ttl is not None:
        cache_doc = assoc("ttl", ttl, cache_doc)

    hyperRequest: HyperRequest = {
        "service": "cache",
        "method": "POST",
        "body": cache_doc,
        "resource": None,
        "params": None,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]
    body = hyperRequestParams["options"]["body"]

    return requests.post(url, headers=headers, data=json.dumps(body))


@promisify
def get_cache(key: str, connection_string: str, domain: str = "default"):

    hyperRequest: HyperRequest = {
        "service": "cache",
        "method": "GET",
        "body": None,
        "resource": key,
        "params": None,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    return requests.get(url, headers=headers)


@promisify
def remove_cache(key: str, connection_string: str, domain: str = "default"):

    hyperRequest: HyperRequest = {
        "service": "cache",
        "method": "DELETE",
        "body": None,
        "resource": key,
        "params": None,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    return requests.delete(url, headers=headers)


@promisify
def set_cache(
    key: str,
    value: Dict,
    ttl: Optional[str],
    connection_string: str,
    domain: str = "default",
):

    if ttl is not None:
        params = {"ttl": ttl}
    else:
        params = None

    # if isinstance(value, dict):
    #     value = json.dumps(value)

    hyperRequest: HyperRequest = {
        "service": "cache",
        "method": "PUT",
        "body": value,
        "resource": key,
        "params": params,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    result = requests.put(url, headers=headers, data=json.dumps(value))
    return result


@promisify
def post_cache_query(
    pattern: Optional[str],
    connection_string: str,
    domain: str = "default",
):

    if pattern is None:
        pattern = "*"

    hyperRequest: HyperRequest = {
        "service": "cache",
        "method": "POST",
        "body": None,
        "resource": None,
        "params": {"pattern": pattern},
        "action": "_query",
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]
    body = hyperRequestParams["options"]["body"]

    results = requests.post(url, headers=headers, data=json.dumps(body))

    data = json.dumps(body)
    return results
