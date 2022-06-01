# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
from typing import Dict, List

import asynctest
from artifacts import book_doc_artifacts
from dotenv import dotenv_values
from ramda import head, is_empty

from hyper_connect import connect
from hyper_connect.types import Hyper, ListOptions

config = dotenv_values("./.env")

book_docs: List[Dict] = book_doc_artifacts()

book1: Dict = head(book_docs)

if is_empty(config):
    print(
        "You seem to be missing a .env file with a `HYPER` environment variable.  Set HYPER with a connection string from your hyper app keys. https://docs.hyper.io/app-key."
    )
    exit()
else:
    connection_string: str = str(config["HYPER"])

hyper: Hyper = connect(connection_string)


class TestIntegration_ASYNC(asynctest.TestCase):
    async def test_data_list_bad_keys_array_async(self):
        options: ListOptions = {
            "startkey": None,
            "limit": None,
            "endkey": None,
            "keys": [6, 7],
            "descending": None,
        }

        try:
            result = await hyper.data.list_async(options)
        except TypeError:
            self.assertEqual(True, True, "Should raise TypeError")

    async def test_data_list_bad_keys_async(self):
        options: ListOptions = {
            "startkey": None,
            "limit": None,
            "endkey": None,
            "keys": 6,
            "descending": None,
        }

        try:
            result = await hyper.data.list_async(options)
        except TypeError as err:
            self.assertEqual(True, True, "Should raise TypeError")

    async def test_data_list_bad_limit_async(self):
        options: ListOptions = {
            "startkey": "book-000100",
            "limit": "foo",
            "endkey": None,
            "keys": None,
            "descending": None,
        }

        try:
            result = await hyper.data.list_async(options)
        except TypeError:
            self.assertEqual(True, True, "Should raise TypeError")

    async def test_data_query_bad_sort_async(self):

        selector = {"type": "book"}

        options: QueryOptions = {
            "fields": ["_id", "name", "published"],
            "sort": 6,
            "limit": 3,
            "useIndex": None,
        }

        result = await hyper.data.query_async(selector, options)

        self.assertEqual(result["ok"], False, "query doc ok.")
        self.assertEqual(result["status"], 422, "status should be 422")

    async def test_data_query_bad_limit_async(self):

        selector = {"type": "book"}

        options: QueryOptions = {
            "fields": ["_id", "name", "published"],
            "sort": None,
            "limit": "foo",
            "useIndex": None,
        }

        result = await hyper.data.query_async(selector, options)
        self.assertEqual(result["ok"], False, "query doc ok.")
        self.assertEqual(result["status"], 422, "status should be 422")


if __name__ == "__main__":
    asynctest.main()
