import io

import requests
from promisio import promisify
from requests_toolbelt.multipart.encoder import MultipartEncoder

from hyper_connect.types import HyperRequest, HyperRequestParams
from hyper_connect.utils import create_hyper_request_params


@promisify
def upload_async(
    name: str,
    data: io.BufferedReader,
    connection_string: str,
    domain: str = "default",
):
    return upload(name, data, connection_string, domain)


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

    return requests.post(url, headers=headers, data=m)


@promisify
def download_async(
    name: str,
    connection_string: str,
    domain: str = "default",
):
    return download(name, connection_string, domain)


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

    return requests.get(url, headers=headers, stream=True)


@promisify
def remove_storage_async(
    name: str,
    connection_string: str,
    domain: str = "default",
):
    return remove_storage(name, connection_string, domain)


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

    return requests.delete(url, headers=headers)
