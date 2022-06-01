# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
from typing import Dict, List

import asynctest
from artifacts import book_doc_artifacts
from dotenv import dotenv_values
from promisio import Promise
from ramda import head, is_empty, map, sum

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


class TestCacheIntegration_ASYNC(asynctest.TestCase):
    async def test_cache_add_async(self):
        # Remove all book docs
        remove_promises = []

        for book_doc in book_docs:
            remove_promises.append(
                hyper.cache.remove_async(key=book_doc["_id"])
            )

        remove_promises_result = await Promise.all_settled(remove_promises)

        # Add all book docs
        add_promises = []
        for book_doc in book_docs:
            add_promises.append(
                hyper.cache.add_async(
                    key=book_doc["_id"], value=book_doc, ttl="1d"
                )
            )

        add_promises_result = await Promise.all_settled(add_promises)

        countFulfilled = sum(
            map(lambda x: x["status"] == "fulfilled", add_promises_result)
        )

        self.assertEqual(countFulfilled, len(book_docs), "Adding docs not ok.")

    async def test_cache_get_async(self):
        result = await hyper.cache.get_async(book1["_id"])
        self.assertEqual(book1["_id"], "book-000100", "Getting doc not ok.")

    async def test_cache_update_async(self):
        result = await hyper.cache.set_async(book1["_id"], book1, ttl="1d")
        self.assertEqual(result["ok"], True, "Update doc not ok.")

    async def test_cache_query_async(self):
        result = await hyper.cache.query_async("book-0001*")

        self.assertEqual(result["ok"], True, "cache query result not ok.")
        self.assertEqual(
            len(result["docs"]) <= 7,
            True,
            "cache query docs length should 6 (after delete) or 7",
        )

    async def test_cache_delete_async(self):
        result = await hyper.cache.remove_async("book-000101")
        self.assertEqual(result["ok"], True, "Removing cached doc not ok.")


if __name__ == "__main__":
    asynctest.main()
