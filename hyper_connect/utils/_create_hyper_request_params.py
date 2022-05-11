from typing import Dict, Optional
from urllib.parse import urlencode, urlparse

from ramda import has, join, omit, pick_by

from hyper_connect.types import (
    Action,
    HyperRequest,
    HyperRequestParams,
    Method,
    RequestOptions,
)

from ._generate_token import decode_token, generate_token
from ._get_host import get_host
from ._get_key import get_key
from ._get_secret import get_secret

# from ramda import is_empty  # type: ignore


def create_hyper_request_params(
    connection_string: str, domain: str, req_params: HyperRequest
) -> HyperRequestParams:
    parsed_url = urlparse(connection_string)
    is_cloud: bool
    protocol: str
    public_key: Optional[str]
    secret: Optional[str]
    token: str
    host: Optional[str]
    pathname: str
    service: str
    appdomain: str
    params: Optional[str]
    url: str
    resource: Optional[str]
    action: Optional[Action]

    if parsed_url.scheme == "cloud":
        is_cloud = True
        protocol = "https:"
    else:
        is_cloud = False
        protocol = f"{parsed_url.scheme}:"

    headers: Dict[str, str] = {"Content-Type": "application/json"}

    public_key = get_key(parsed_url.netloc)
    secret = get_secret(parsed_url.netloc)

    if public_key is not None and secret is not None:

        token = generate_token(public_key, secret)
        # print('minty fresh token: ' + token)

        # decoded_token: Dict[str, Any] = decode_token(token, secret)
        # print('decoded_token below')
        # print(decoded_token)
        # print('exp: ', decoded_token["exp"])
        # print(datetime.fromtimestamp(decoded_token["exp"], timezone.utc))

        headers["Authorization"] = f"Bearer {token}"

        # print(headers)

    host = get_host(parsed_url.netloc)

    if is_cloud == True:
        pathname = parsed_url.path
        appdomain = f"/{domain}"
    else:
        pathname = ""
        appdomain = parsed_url.path

    service = req_params["service"]

    if req_params["service"] == "info":
        url = f"{protocol}//{host}"
    else:
        url = f"{protocol}//{host}{pathname}/{service}{appdomain}"

    resource = req_params["resource"]
    action = req_params["action"]
    if resource is not None:
        url = f"{url}/{resource}"
    elif action is not None:

        url = f"{url}/{action}"

    if req_params["params"] is not None:
        # Convert a mapping object or a sequence of two-element tuples,
        # which may contain str or bytes objects, to a percent-encoded ASCII text string.
        print('req_params["params"] is not None', req_params["params"])

        def not_none_value(val, key):
            return val is not None

        tasty_params = pick_by(not_none_value, req_params["params"])

        if "keys" in tasty_params:
            if type(tasty_params["keys"]) is list:
                tasty_params["keys"] = join(",", tasty_params["keys"])

        print("tasty_params:", tasty_params)

        params = urlencode(tasty_params)
        url = f"{url}?{params}"

        print("url: ", url)
        # params = urlencode(req_params["params"])
        # url = f"{url}?{params}"

    requestOptions = RequestOptions(
        {
            "headers": headers,
            "method": req_params["method"],
            "body": req_params["body"],
        }
    )

    hyperRequestParams = HyperRequestParams({"url": url, "options": requestOptions})

    return hyperRequestParams
