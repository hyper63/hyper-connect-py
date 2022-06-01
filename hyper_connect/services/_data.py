import json
from typing import Dict, List

import requests
from promisio import promisify

from hyper_connect.types import (
    HyperRequest,
    HyperRequestParams,
    ListOptions,
    QueryOptions,
)
from hyper_connect.utils import create_hyper_request_params, to_data_query


@promisify
def add_data_async(
    body: Dict, connection_string: str, domain: str = "default"
):
    result = add_data(body, connection_string, domain)
    return result


def add_data(body: Dict, connection_string: str, domain: str = "default"):

    hyperRequest: HyperRequest = {
        "service": "data",
        "method": "POST",
        "body": body,
        "resource": None,
        "params": None,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    # Example HyperRequestParams
    # {
    #     'url': 'https://cloud.hyper.io/express-quickstart/data/default',
    #     'options': {
    #         'headers': {
    #             'Content-Type': 'application/json',
    #             'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ4bWd0YTBudW02ajduNnVuN2FhNm91Z2EyNnZxbjc4NCIsImV4cCI6MTY1MTc2NTAwMX0.ChZqjXFOJDYFgsHMFHLTk_iIRR-qW1BfRutJxMObvqE'
    #             },
    #         'method': 'GET',
    #         'body': 'foo bar'
    #     }
    # }

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    return requests.post(url, headers=headers, data=json.dumps(body))


@promisify
def get_data_async(id: str, connection_string: str, domain: str = "default"):
    return get_data(id, connection_string, domain)


def get_data(id: str, connection_string: str, domain: str = "default"):

    hyperRequest: HyperRequest = {
        "service": "data",
        "method": "GET",
        "body": None,
        "resource": id,
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
def get_data_list_async(
    options: ListOptions, connection_string: str, domain: str = "default"
):
    return get_data_list(options, connection_string, domain)


def get_data_list(
    options: ListOptions, connection_string: str, domain: str = "default"
):

    hyperRequest: HyperRequest = {
        "service": "data",
        "method": "GET",
        "body": None,
        "resource": None,
        "params": options,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    # Querystring parameters [optional]

    #     limit - {number} default: 1000  - limits the number of documents returned
    #     startkey - {string} key matcher for document id's
    #     endkey -  {string} key matcher for document id's
    #     keys - {array[string]} a collection of key ids for returning documents
    #     descending - {true|false} - determines the order of the list sorted on the 'id' column

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    return requests.get(url, headers=headers)


@promisify
def update_data_async(
    id: str, doc: Dict, connection_string: str, domain: str = "default"
):
    return update_data(id, doc, connection_string, domain)


def update_data(
    id: str, doc: Dict, connection_string: str, domain: str = "default"
):

    hyperRequest: HyperRequest = {
        "service": "data",
        "method": "PUT",
        "body": doc,
        "resource": id,
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
def remove_data_async(
    id: str, connection_string: str, domain: str = "default"
):
    return remove_data(id, connection_string, domain)


def remove_data(id: str, connection_string: str, domain: str = "default"):

    hyperRequest: HyperRequest = {
        "service": "data",
        "method": "DELETE",
        "body": None,
        "resource": id,
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
def post_query_async(
    selector: Dict,
    options: QueryOptions,
    connection_string: str,
    domain: str = "default",
):
    return post_query(selector, options, connection_string, domain)


def post_query(
    selector: Dict,
    options: QueryOptions,
    connection_string: str,
    domain: str = "default",
):

    data_query: Dict = to_data_query(selector, options)

    hyperRequest: HyperRequest = {
        "service": "data",
        "method": "POST",
        "body": data_query,
        "resource": None,
        "params": None,
        "action": "_query",
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]
    body = hyperRequestParams["options"]["body"]

    return requests.post(url, headers=headers, data=json.dumps(body))


@promisify
def post_index_async(
    name: str,
    fields: List[str],
    connection_string: str,
    domain: str = "default",
):
    return post_index(name, fields, connection_string, domain)


def post_index(
    name: str,
    fields: List[str],
    connection_string: str,
    domain: str = "default",
):
    indexBody: Dict = {"name": name, "type": "json", "fields": fields}

    hyperRequest: HyperRequest = {
        "service": "data",
        "method": "POST",
        "body": indexBody,
        "resource": None,
        "params": None,
        "action": "_index",
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]
    body = hyperRequestParams["options"]["body"]

    return requests.post(url, headers=headers, data=json.dumps(body))


@promisify
def post_bulk_async(
    docs: List[Dict],
    connection_string: str,
    domain: str = "default",
):
    return post_bulk(docs, connection_string, domain)


def post_bulk(
    docs: List[Dict],
    connection_string: str,
    domain: str = "default",
):

    hyperRequest: HyperRequest = {
        "service": "data",
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
    return results
