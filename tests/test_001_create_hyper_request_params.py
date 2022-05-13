# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v

import unittest
from typing import Dict

from ramda import head, split  # type: ignore

from hyper_connect.types import HyperRequest, HyperRequestParams
from hyper_connect.utils import create_hyper_request_params

body: Dict = {
    "_id": "book-102",
    "type": "book",
    "name": "Horton hears a who 2",
    "author": "Dr. Suess",
    "published": "1953",
}

expected_result: HyperRequestParams = {
    "url": "https://cloud.hyper.io/express-quickstart/data/default",
    "options": {
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ4bWd0YTBudW02ajduNnVuN2FhNm91Z2EyNnZxbjc4NCIsImV4cCI6MTY1MTg3MTkyMX0.tlfSFwX5uXcHxgLu8oTteTl35nNHlWN8XH7d3i36MAY",
        },
        "method": "POST",
        "body": {
            "_id": "book-102",
            "type": "book",
            "name": "Horton hears a who 2",
            "author": "Dr. Suess",
            "published": "1953",
        },
    },
}

hyperRequest: HyperRequest = {
    "service": "data",
    "method": "POST",
    "body": body,
    "resource": None,
    "params": None,
    "action": None,
}


class TestCreateHyperRequestParams(unittest.TestCase):
    def test_happy_data_post_url(self):
        hyperRequestParams: HyperRequestParams = create_hyper_request_params(
            "cloud://xmgta0num6j7n6un7aa6ouga26vqn784:cADh5FHDPWr5jE6qLDmCqQlMRkfUEWMsLPRaZ64EGFZImvUBx--gI1MkcrUqFPMR@cloud.hyper.io/express-quickstart",
            "default",
            hyperRequest,
        )

        self.assertEqual(
            hyperRequestParams["url"], expected_result["url"], "url Not equal"
        )

    def test_happy_data_post_body(self):
        hyperRequestParams: HyperRequestParams = create_hyper_request_params(
            "cloud://xmgta0num6j7n6un7aa6ouga26vqn784:cADh5FHDPWr5jE6qLDmCqQlMRkfUEWMsLPRaZ64EGFZImvUBx--gI1MkcrUqFPMR@cloud.hyper.io/express-quickstart",
            "default",
            hyperRequest,
        )

        self.assertEqual(
            hyperRequestParams["options"]["body"],
            expected_result["options"]["body"],
            "Body Not equal",
        )

    def test_happy_data_post_auth_bearer(self):
        hyperRequestParams: HyperRequestParams = create_hyper_request_params(
            "cloud://xmgta0num6j7n6un7aa6ouga26vqn784:cADh5FHDPWr5jE6qLDmCqQlMRkfUEWMsLPRaZ64EGFZImvUBx--gI1MkcrUqFPMR@cloud.hyper.io/express-quickstart",
            "default",
            hyperRequest,
        )

        self.assertEqual(
            head(split(" ", hyperRequestParams["options"]["headers"]["Authorization"])),
            "Bearer",
            "Bearer does not exist",
        )


if __name__ == "__main__":
    unittest.main()
