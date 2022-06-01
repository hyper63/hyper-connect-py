# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
import unittest
from typing import Dict, List

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


class TestDataIntegration_SYNC(unittest.TestCase):
    def test_data_add_sync(self):

        remove_result = hyper.data.remove(id=book1["_id"])
        add_result = hyper.data.add(doc=book1)

        self.assertEqual(
            remove_result["ok"], True, "SYNC Removing data doc not ok."
        )
        self.assertEqual(
            add_result["ok"], True, "SYNC Adding data doc not ok."
        )

    def test_data_get_sync(self):
        result = hyper.data.get(book1["_id"])
        self.assertEqual(book1["_id"], result["_id"], "Getting doc not ok.")

    # def test_data_update_sync(self):
    #     result = hyper.data.update(book1["_id"], book1)
    #     self.assertEqual(result["ok"], True, "Update doc not ok.")

    # def test_data_list_startkey_endkey_sync(self):
    #     options: ListOptions = {
    #         "startkey": "book-000105",
    #         "limit": None,
    #         "endkey": "book-000106",
    #         "keys": None,
    #         "descending": None,
    #     }

    #     result = hyper.data.list(options)
    #     self.assertEqual(result["ok"], True, "List result not ok.")
    #     self.assertEqual(len(result["docs"]), 2, "Length should be 2")

    # def test_data_list_keys_array_sync(self):
    #     options: ListOptions = {
    #         "startkey": None,
    #         "limit": None,
    #         "endkey": None,
    #         "keys": ["book-000105", "book-000106"],
    #         "descending": None,
    #     }

    #     result = hyper.data.list(options)
    #     self.assertEqual(result["ok"], True, "List result not ok.")
    #     self.assertEqual(len(result["docs"]), 2, "Length should be 2")

    # def test_data_list_keys_comma_list_sync(self):
    #     options: ListOptions = {
    #         "startkey": None,
    #         "limit": None,
    #         "endkey": None,
    #         "keys": ["book-000105,book-000106"],
    #         "descending": None,
    #     }

    #     result = hyper.data.list(options)
    #     self.assertEqual(result["ok"], True, "List result not ok.")
    #     self.assertEqual(len(result["docs"]), 2, "Length should be 2")

    # def test_data_list_limit_sync(self):
    #     options: ListOptions = {
    #         "startkey": "book-000100",
    #         "limit": 4,
    #         "endkey": None,
    #         "keys": None,
    #         "descending": None,
    #     }

    #     result = hyper.data.list(options)

    #     self.assertEqual(result["ok"], True, "List result not ok.")
    #     self.assertEqual(len(result["docs"]), 4, "Length should be 4")

    # def test_data_query_limit_10_sync(self):

    #     selector = {"type": "book", "name": {"$eq": "The Lorax 103"}}

    #     options: QueryOptions = {
    #         "fields": None,
    #         "sort": None,
    #         "limit": 10,
    #         "useIndex": None,
    #     }

    #     result = hyper.data.query(selector, options)

    #     self.assertEqual(result["ok"], True, "Query result not ok.")
    #     self.assertEqual(len(result["docs"]), 1, "Length should be 1")

    # def test_data_query_fields_sync(self):

    #     selector = {"type": "book"}

    #     options: QueryOptions = {
    #         "fields": ["_id", "name", "published"],
    #         "sort": None,
    #         "limit": 3,
    #         "useIndex": None,
    #     }

    #     result = hyper.data.query(selector, options)

    #     self.assertEqual(result["ok"], True, "Query result not ok.")
    #     self.assertEqual(len(result["docs"]), 3, "Length should be 3")
    #     self.assertEqual(
    #         len(keys(head(result["docs"]))),
    #         3,
    #         "There should be 3 keys in a doc.",
    #     )

    # def test_data_query_index_sync(self):

    #     selector = {"type": "book", "author": "James A. Michener"}

    #     options: QueryOptions = {
    #         "fields": ["author", "published"],
    #         "sort": [{"author": "DESC"}, {"published": "DESC"}],
    #         "useIndex": "idx_author_published",
    #     }

    #     index_result = hyper.data.index(
    #         "idx_author_published", ["author", "published"]
    #     )

    #     result = hyper.data.query(selector, options)

    #     self.assertEqual(
    #         index_result["ok"], True, "index create result not ok."
    #     )
    #     self.assertEqual(len(result["docs"]), 3, "Length should be 3")
    #     self.assertEqual(
    #         len(keys(head(result["docs"]))),
    #         2,
    #         "There should be 2 keys in a doc.",
    #     )
    #     self.assertEqual(
    #         prop("published", head(result["docs"])),
    #         "1985",
    #         "The first doc should be published in 1985",
    #     )

    # def test_bulk_data_sync(self):

    #     # Bulk remove docs
    #     bulkDocs = map(
    #         lambda doc: assoc("_deleted", True, doc), book_bulk_docs
    #     )

    #     bulk_result = hyper.data.bulk(bulkDocs)
    #     book_bulk_result = hyper.data.bulk(book_bulk_docs)

    #     self.assertEqual(book_bulk_result["ok"], True, "Bulk result not ok.")
    #     self.assertEqual(len(book_bulk_result["results"]), 3, "Length should be 3.")

    #     # {"ok":true,"results":[{"ok":true,"id":"movie-4"}]}

    #     def by_ok(r):
    #         if r["ok"] is True:
    #             return "true"
    #         else:
    #             return "false"

    #     number_of_true_results = compose(
    #         prop("true"), count_by(by_ok), prop_or([], "results")
    #     )(book_bulk_result)

    #     self.assertEqual(
    #         number_of_true_results,
    #         3,
    #         "There should be 3 ok results.",
    #     )


if __name__ == "__main__":
    unittest.main()
