from promisio import Promise
from ramda import if_else
from requests import HTTPError

# class InternalServerError(Exception):
#     """Exception raised for 500 level HTTP errors when attempting to call hyper REST API.

#     Attributes:
#         status -- 500 level http status code
#         message -- explanation of the error
#     """

#     def __init__(, status, message)


def handle_response(response):

    # print('type(response): ', type(response)). #  <class 'requests.models.Response'>

    content_type_is_application_json = lambda x: "application/json" in x.headers.get(
        "content-type"
    )
    to_json = lambda x: x.json()

    def to_ok(x):
        return {"ok": x.ok, "msg": x.text}

    def check_response_ok_add_status(r):
        if response.ok:
            return r
        else:
            r["status"] = response.status_code
            return r

    def check_500_error(r):
        if response.status_code >= 500:

            print("check_500_error occurred!!!", response)
            return Promise.reject(response.raise_for_status())
        else:
            return r

    return (
        Promise.resolve(response)
        .then(if_else(content_type_is_application_json, to_json, to_ok))
        .then(check_response_ok_add_status)
        .then(check_500_error)
    )
