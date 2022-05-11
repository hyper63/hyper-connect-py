from typing import Any, Dict, Optional, TypedDict

import requests
from promisio import promisify

from hyper_connect.types import HyperRequest, HyperRequestParams, ListOptions
from hyper_connect.utils import check_json, create_hyper_request_params


@promisify
def addData(body: str, connection_string: str, domain: str = "default"):

    check_json_result: bool = check_json(body)

    if not check_json_result:
        raise ValueError("body should be a should be a json string.")

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
    # print('inside _data.py addData() hyperRequestParams dict')

    # for k, v in hyperRequestParams.items():
    #     print(k, v)

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    return requests.post(url, headers=headers, data=body)


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
    # print('inside _data.py addData() hyperRequestParams dict')

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    return requests.get(url, headers=headers)


@promisify
def getDataList(options: ListOptions, connection_string: str, domain: str = "default"):

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
