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
def addData(body: Dict, connection_string: str, domain: str = "default"):

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
def getDataById(id: str, connection_string: str, domain: str = "default"):

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
def getDataList(
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
def updateData(
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
def removeDataById(id: str, connection_string: str, domain: str = "default"):

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
def postQuery(
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

    results = requests.post(url, headers=headers, data=json.dumps(body))

    data = json.dumps(body)
    return results.json()


@promisify
def postIndex(
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

    results = requests.post(url, headers=headers, data=json.dumps(body))
    return results.json()


@promisify
def postBulk(
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
    return results.json()
