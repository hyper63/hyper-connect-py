# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
import json
from typing import Any, Dict, List, Optional

import asynctest
from artifacts import book_doc_artifact
from dotenv import dotenv_values
from promisio import Promise
from ramda import (
    compose,
    has,
    head,
    is_empty,
    join,
    map,
    merge,
    pick_by,
    prop,
    prop_or,
    sum,
)

from hyper_connect import connect
from hyper_connect.types import Hyper, ListOptions, QueryOptions

config = dotenv_values("./.env")

book_docs: List[Dict] = book_doc_artifact()

book1: Dict = head(book_docs)

if is_empty(config):
    print(
        "You seem to be missing a .env file with a `HYPER` environment variable.  Set HYPER with a connection string from your hyper app keys. https://docs.hyper.io/app-key."
    )
    exit()
else:
    connection_string: str = str(config["HYPER"])

hyper: Hyper = connect(connection_string)


class TestIntegration(asynctest.TestCase):
    async def test_data_add(self):

        # Remove all book docs
        remove_promises = []

        for book_doc in book_docs:
            remove_promises.append(hyper.data.remove(book_doc["_id"]))

        remove_promises_result = await Promise.all_settled(remove_promises)

        # Add all book docs
        add_promises = []
        for book_doc in book_docs:
            add_promises.append(hyper.data.add(book_doc))

        add_promises_result = await Promise.all_settled(add_promises)

        countFulfilled = sum(
            map(lambda x: x["status"] == "fulfilled", add_promises_result)
        )

        self.assertEqual(countFulfilled, len(book_docs), "Adding docs not ok.")

    async def test_data_get(self):
        result = await hyper.data.get(book1["_id"])
        self.assertEqual(book1["_id"], "book-000100", "Getting doc not ok.")

    async def test_data_update(self):
        result = await hyper.data.update(book1["_id"], book1)
        self.assertEqual(result["ok"], True, "Update doc not ok.")

    async def test_data_list_startkey(self):
        options: ListOptions = {
            "startkey": "movie-5",
            "limit": None,
            "endkey": None,
            "keys": None,
            "descending": None,
        }

        result = await hyper.data.list(options)
        self.assertEqual(result["ok"], True, "List startkey doc not ok.")


if __name__ == "__main__":
    asynctest.main()
