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
def add_search_async(
    key: str, doc: Dict, connection_string: str, domain: str = "default"
):
    result = add_search(key, doc, connection_string, domain)
    return result


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
def get_search_async(
    key: str, connection_string: str, domain: str = "default"
):
    return get_search(key, connection_string, domain)


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

    return requests.get(url, headers=headers)


@promisify
def update_search_async(
    key: str, doc: Dict, connection_string: str, domain: str = "default"
):
    return update_search(key, doc, connection_string, domain)


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

    return requests.put(url, headers=headers, data=json.dumps(doc))


@promisify
def remove_search_async(
    key: str, connection_string: str, domain: str = "default"
):
    return remove_search(key, connection_string, domain)


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

    return requests.delete(url, headers=headers)


@promisify
def post_query_search_async(
    query: str,
    options: Optional[SearchQueryOptions],
    connection_string: str,
    domain: str = "default",
):
    return post_query_search(query, options, connection_string, domain)


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

    return requests.post(url, headers=headers, data=json.dumps(body))


@promisify
def load_search_async(
    docs: List[Dict],
    connection_string: str,
    domain: str = "default",
):
    return load_search(docs, connection_string, domain)


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

    return requests.post(url, headers=headers, data=json.dumps(body))
