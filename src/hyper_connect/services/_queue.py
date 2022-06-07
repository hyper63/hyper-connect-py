import json
from typing import Dict

import requests
from promisio import promisify

from hyper_connect.types import HyperRequest, HyperRequestParams
from hyper_connect.utils import create_hyper_request_params


@promisify
def queue_enqueue_async(
    job: Dict, connection_string: str, domain: str = "default"
):
    return queue_enqueue(job, connection_string, domain)


def queue_enqueue(job: Dict, connection_string: str, domain: str = "default"):

    hyperRequest: HyperRequest = {
        "service": "queue",
        "method": "POST",
        "body": job,
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
def queue_errors_async(connection_string: str, domain: str = "default"):
    return queue_errors(connection_string, domain)


def queue_errors(connection_string: str, domain: str = "default"):

    hyperRequest: HyperRequest = {
        "service": "queue",
        "method": "GET",
        "body": None,
        "resource": None,
        "params": {"status": "ERROR"},
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    return requests.get(url, headers=headers)


@promisify
def queue_queued_async(connection_string: str, domain: str = "default"):
    queue_queued(connection_string, domain)


def queue_queued(connection_string: str, domain: str = "default"):

    hyperRequest: HyperRequest = {
        "service": "queue",
        "method": "GET",
        "body": None,
        "resource": None,
        "params": {"status": "READY"},
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    return requests.get(url, headers=headers)
