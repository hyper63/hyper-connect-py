import io
import json
from typing import Any, Dict, List, Optional, Union

import requests
from promisio import promisify
from ramda import merge
from requests_toolbelt.multipart.encoder import MultipartEncoder

from hyper_connect.types import HyperRequest, HyperRequestParams
from hyper_connect.utils import create_hyper_request_params


@promisify
def upload(
    name: str,
    data: io.BufferedReader,
    connection_string: str,
    domain: str = "default",
):

    m = MultipartEncoder(fields={"file": (name, data, "text/plain")})

    hyperRequest: HyperRequest = {
        "service": "storage",
        "method": "POST",
        "body": m,
        "resource": None,
        "params": None,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    headers["Content-Type"] = m.content_type

    r = requests.post(url, headers=headers, data=m)

    return r


@promisify
def download(
    name: str,
    connection_string: str,
    domain: str = "default",
):
    hyperRequest: HyperRequest = {
        "service": "storage",
        "method": "GET",
        "body": None,
        "resource": name,
        "params": None,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    r = requests.get(url, headers=headers, stream=True)

    return r


@promisify
def remove_storage(
    name: str,
    connection_string: str,
    domain: str = "default",
):
    hyperRequest: HyperRequest = {
        "service": "storage",
        "method": "DELETE",
        "body": None,
        "resource": name,
        "params": None,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    result = requests.delete(url, headers=headers, stream=True)
    theresult = result.json()

    print("************* theresult", theresult)

    return theresult