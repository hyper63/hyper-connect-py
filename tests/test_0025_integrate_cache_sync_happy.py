# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
import unittest
from typing import Dict, List

from artifacts import book_doc_artifacts
from dotenv import dotenv_values
from ramda import head, is_empty

from hyper_connect import connect
from hyper_connect.types import Hyper

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


class TestCacheIntegration_SYNC(unittest.TestCase):
    def test_cache_add_sync(self):

        remove_result = hyper.cache.remove(key=book1["_id"])
        add_result = hyper.cache.add(key=book1["_id"], value=book1, ttl="1d")

        self.assertEqual(
            remove_result["ok"], True, "SYNC Removing cached doc not ok."
        )
        self.assertEqual(
            add_result["ok"], True, "SYNC Adding cached doc not ok."
        )

    def test_cache_get_sync(self):
        result = hyper.cache.get(key=book1["_id"])
        self.assertEqual(
            book1["_id"], "book-000100", "SYNC Getting doc not ok."
        )

    def test_cache_update_sync(self):
        result = hyper.cache.set(book1["_id"], book1, ttl="1d")
        self.assertEqual(result["ok"], True, "SYNC Update doc not ok.")

    def test_cache_query_sync(self):
        result = hyper.cache.query("book-0001*")
        self.assertEqual(result["ok"], True, "SYNC cache query result not ok.")
        self.assertEqual(
            len(result["docs"]) <= 7,
            True,
            "SYNC cache query docs length should 6 (after delete) or 7",
        )


if __name__ == "__main__":
    unittest.main()
