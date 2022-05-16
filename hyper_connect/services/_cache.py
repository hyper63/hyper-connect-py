import json
from typing import Any, Dict, List, Optional

import requests
from promisio import promisify
from ramda import assoc

from hyper_connect.types import HyperRequest, HyperRequestParams
from hyper_connect.utils import create_hyper_request_params


@promisify
def add_cache(
    key: str,
    value: Any,
    ttl: Optional[str],
    connection_string: str,
    domain: str = "default",
):

    cacheDoc = {"key": key, "value": value}

    if ttl is not None:
        cacheDoc = assoc("ttl", ttl, cacheDoc)

    hyperRequest: HyperRequest = {
        "service": "cache",
        "method": "POST",
        "body": cacheDoc,
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

    return requests.get(url, headers=headers)


@promisify
def set_cache(
    key: str,
    value: Any,
    ttl: Optional[str],
    connection_string: str,
    domain: str = "default",
):

    if ttl is not None:
        params = {"ttl": ttl}
    else:
        params = None

    if isinstance(value, dict):
        value = json.dumps(value)

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

    return requests.post(url, headers=headers, data=value)


@promisify
def post_query(
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
    return results.json()
