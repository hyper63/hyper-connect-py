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

    # m = MultipartEncoder(
    # fields={'field2': (name, open('file.py', 'rb'), 'text/plain')}
    # )

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
    # body = hyperRequestParams["options"]["body"]

    # r = requests.post(url, data=m,
    #                   headers={'Content-Type': m.content_type})

    r = requests.post(url, headers={"Content-Type": m.content_type}, data=m)

    return r
