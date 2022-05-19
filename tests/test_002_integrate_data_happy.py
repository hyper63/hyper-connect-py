# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
import json
from typing import Dict, List

import asynctest
from artifacts import book_bulk_doc_artifacts, book_doc_artifacts
from dotenv import dotenv_values
from promisio import Promise
from ramda import (
    assoc,
    compose,
    count_by,
    head,
    is_empty,
    keys,
    map,
    prop,
    prop_or,
    sum,
)

from hyper_connect import connect
from hyper_connect.types import Hyper, ListOptions

config = dotenv_values("./.env")

book_docs: List[Dict] = book_doc_artifacts()
book_bulk_docs: List[Dict] = book_bulk_doc_artifacts()

book1: Dict = head(book_docs)


if is_empty(config):
    print(
        "You seem to be missing a .env file with a `HYPER` environment variable.  Set HYPER with a connection string from your hyper app keys. https://docs.hyper.io/app-key."
    )
    exit()
else:
    connection_string: str = str(config["HYPER"])

hyper: Hyper = connect(connection_string)


class TestDataIntegration(asynctest.TestCase):
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

    async def test_data_list_startkey_endkey(self):
        options: ListOptions = {
            "startkey": "book-000105",
            "limit": None,
            "endkey": "book-000106",
            "keys": None,
            "descending": None,
        }

        result = await hyper.data.list(options)
        self.assertEqual(result["ok"], True, "List result not ok.")
        self.assertEqual(len(result["docs"]), 2, "Length should be 2")

    async def test_data_list_keys_array(self):
        options: ListOptions = {
            "startkey": None,
            "limit": None,
            "endkey": None,
            "keys": ["book-000105", "book-000106"],
            "descending": None,
        }

        result = await hyper.data.list(options)
        self.assertEqual(result["ok"], True, "List result not ok.")
        self.assertEqual(len(result["docs"]), 2, "Length should be 2")

    async def test_data_list_keys_comma_list(self):
        options: ListOptions = {
            "startkey": None,
            "limit": None,
            "endkey": None,
            "keys": ["book-000105,book-000106"],
            "descending": None,
        }

        result = await hyper.data.list(options)
        self.assertEqual(result["ok"], True, "List result not ok.")
        self.assertEqual(len(result["docs"]), 2, "Length should be 2")

    async def test_data_list_limit(self):
        options: ListOptions = {
            "startkey": "book-000100",
            "limit": 4,
            "endkey": None,
            "keys": None,
            "descending": None,
        }

        result = await hyper.data.list(options)

        self.assertEqual(result["ok"], True, "List result not ok.")
        self.assertEqual(len(result["docs"]), 4, "Length should be 4")

    async def test_data_query_limit_10(self):

        selector = {"type": "book", "name": {"$eq": "The Lorax 103"}}

        options: QueryOptions = {
            "fields": None,
            "sort": None,
            "limit": 10,
            "useIndex": None,
        }

        result = await hyper.data.query(selector, options)

        self.assertEqual(result["ok"], True, "Query result not ok.")
        self.assertEqual(len(result["docs"]), 1, "Length should be 1")

    async def test_data_query_fields(self):

        selector = {"type": "book"}

        options: QueryOptions = {
            "fields": ["_id", "name", "published"],
            "sort": None,
            "limit": 3,
            "useIndex": None,
        }

        result = await hyper.data.query(selector, options)

        self.assertEqual(result["ok"], True, "Query result not ok.")
        self.assertEqual(len(result["docs"]), 3, "Length should be 3")
        self.assertEqual(
            len(keys(head(result["docs"]))),
            3,
            "There should be 3 keys in a doc.",
        )

    async def test_data_query_index(self):

        selector = {"type": "book", "author": "James A. Michener"}

        options: QueryOptions = {
            "fields": ["author", "published"],
            "sort": [{"author": "DESC"}, {"published": "DESC"}],
            "useIndex": "idx_author_published",
        }

        index_result = await hyper.data.index(
            "idx_author_published", ["author", "published"]
        )

        result = await hyper.data.query(selector, options)

        self.assertEqual(
            index_result["ok"], True, "index create result not ok."
        )
        self.assertEqual(len(result["docs"]), 3, "Length should be 3")
        self.assertEqual(
            len(keys(head(result["docs"]))),
            2,
            "There should be 2 keys in a doc.",
        )
        self.assertEqual(
            prop("published", head(result["docs"])),
            "1985",
            "The first doc should be published in 1985",
        )

    async def test_bulk_data(self):

        # Bulk remove docs
        bulkDocs = map(
            lambda doc: assoc("_deleted", True, doc), book_bulk_docs
        )

        result = await hyper.data.bulk(bulkDocs).then(
            lambda _: hyper.data.bulk(book_bulk_docs)
        )

        self.assertEqual(result["ok"], True, "Bulk result not ok.")
        self.assertEqual(len(result["results"]), 3, "Length should be 3.")

        # {"ok":true,"results":[{"ok":true,"id":"movie-4"}]}

        def by_ok(r):
            if r["ok"] is True:
                return "true"
            else:
                return "false"

        number_of_true_results = compose(
            prop("true"), count_by(by_ok), prop_or([], "results")
        )(result)

        self.assertEqual(
            number_of_true_results,
            3,
            "There should be 3 ok results.",
        )


if __name__ == "__main__":
    asynctest.main()
