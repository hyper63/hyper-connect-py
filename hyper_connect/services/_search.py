import json
from typing import Any, Dict, List, Optional

import requests
from promisio import promisify
from ramda import merge

from hyper_connect.types import (
    HyperRequest,
    HyperRequestParams,
    SearchQueryOptions,
)
from hyper_connect.utils import create_hyper_request_params


@promisify
def add_search(
    key: str, doc: Dict, connection_string: str, domain: str = "default"
):

    hyperRequest: HyperRequest = {
        "service": "search",
        "method": "POST",
        "body": {"key": key, "doc": doc},
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
def get_search(key: str, connection_string: str, domain: str = "default"):

    hyperRequest: HyperRequest = {
        "service": "search",
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

    result = requests.get(url, headers=headers)

    return result.json()


@promisify
def update_search(
    key: str, doc: Dict, connection_string: str, domain: str = "default"
):

    hyperRequest: HyperRequest = {
        "service": "search",
        "method": "PUT",
        "body": doc,
        "resource": key,
        "params": None,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    result = requests.put(url, headers=headers, data=json.dumps(doc))
    return result.json()


@promisify
def remove_search(key: str, connection_string: str, domain: str = "default"):

    hyperRequest: HyperRequest = {
        "service": "search",
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

    result = requests.delete(url, headers=headers)
    return result.json()


@promisify
def post_query_search(
    query: str,
    options: Optional[SearchQueryOptions],
    connection_string: str,
    domain: str = "default",
):

    # {
    #     "query": "Ghostbusters",
    #     "fields": ["title"],
    #     "filter": {"year": "1984"}
    # }

    search_body = {"query": query}

    if options is not None:
        search_body = merge(search_body, options)

    hyperRequest: HyperRequest = {
        "service": "search",
        "method": "POST",
        "body": search_body,
        "resource": None,
        "params": None,
        "action": "_query",
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]
    body: Any = hyperRequestParams["options"]["body"]

    results = requests.post(url, headers=headers, data=json.dumps(body))

    return results.json()


@promisify
def load_search(
    docs: List[Dict],
    connection_string: str,
    domain: str = "default",
):

    hyperRequest: HyperRequest = {
        "service": "search",
        "method": "POST",
        "body": docs,
        "resource": None,
        "params": None,
        "action": "_bulk",
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]
    body = hyperRequestParams["options"]["body"]

    results = requests.post(url, headers=headers, data=json.dumps(body))
    return results.json()