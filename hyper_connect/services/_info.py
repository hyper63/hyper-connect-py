import requests
from promisio import promisify

from hyper_connect.types import HyperRequest, HyperRequestParams
from hyper_connect.utils import create_hyper_request_params


@promisify
def services_async(
    connection_string: str,
    domain: str = "default",
):
    result = services(connection_string, domain)
    return result


def services(
    connection_string: str,
    domain: str = "default",
):
    hyperRequest: HyperRequest = {
        "service": "info",
        "method": "GET",
        "body": None,
        "resource": None,
        "params": None,
        "action": None,
    }
    hyperRequestParams: HyperRequestParams = create_hyper_request_params(
        connection_string, domain, hyperRequest
    )

    url: str = hyperRequestParams["url"]
    headers = hyperRequestParams["options"]["headers"]

    return requests.get(url, headers=headers)
