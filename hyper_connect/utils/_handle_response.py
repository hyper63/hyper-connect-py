from promisio import Promise
from ramda import if_else


def handle_response(response):
    # content_type_is_application_json = (
    #     lambda x: "application/json" in x.headers.get("content-type")
    # )

    def content_type_is_application_json(x):
        if "application/json" in x.headers.get("content-type"):
            return True
        else:
            return False

    to_json = lambda x: x.json()

    def to_ok(x):
        return {"ok": x.ok, "msg": x.text}

    def check_response_ok_add_status(r):

        if response.ok:
            r["status"] = response.status_code
            return r
        else:
            r["status"] = response.status_code
            return r

    def check_500_error(r):
        if response.status_code >= 500:
            return Promise.reject(response.raise_for_status())
        else:
            return r

    return (
        Promise.resolve(response)
        .then(if_else(content_type_is_application_json, to_json, to_ok))
        .then(check_response_ok_add_status)
        .then(check_500_error)
    )
