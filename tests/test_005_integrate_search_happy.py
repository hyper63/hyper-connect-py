# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
import json
from typing import Dict, List

import asynctest
from artifacts import movie_doc_artifacts
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

movie_docs: List[Dict] = movie_doc_artifacts()

movie1: Dict = head(movie_docs)

if is_empty(config):
    print(
        "You seem to be missing a .env file with a `HYPER` environment variable.  Set HYPER with a connection string from your hyper app keys. https://docs.hyper.io/app-key."
    )
    exit()
else:
    connection_string: str = str(config["HYPER"])

hyper: Hyper = connect(connection_string)


class TestSearchIntegration(asynctest.TestCase):
    async def test_search_add(self):
        # Remove all book docs
        remove_promises = []

        for movie_doc in movie_docs:
            remove_promises.append(hyper.search.remove(key=movie_doc["_id"]))

        remove_promises_result = await Promise.all_settled(remove_promises)

        # Add all book docs
        add_promises = []
        for movie_doc in movie_docs:
            add_promises.append(
                hyper.search.add(key=movie_doc["_id"], doc=movie_doc)
            )

        add_promises_result = await Promise.all_settled(add_promises)

        countFulfilled = sum(
            map(lambda x: x["status"] == "fulfilled", add_promises_result)
        )

        self.assertEqual(
            countFulfilled, len(movie_docs), "Adding docs to search not ok."
        )

    async def test_search_get(self):
        result = await hyper.search.get(movie1["_id"])

        # {'key': 'movie-100', 'doc': {'type': 'movie', 'title': 'Chariots of Fire', 'year': '1981', '_id': 'movie-100'}, 'ok': True}
        # update_result = await hyper.search.update(movie1["_id"], movie1)
        # print('update_result: ', update_result)
        # self.assertEqual(update_result["ok"], True, "Update doc not ok.")

        doc = result["doc"]

        self.assertEqual(
            doc["title"],
            "Chariots of Fire",
            "Getting doc from search not ok.",
        )

    # async def test_data_list_keys_array(self):
    #     options: ListOptions = {
    #         "startkey": None,
    #         "limit": None,
    #         "endkey": None,
    #         "keys": ["book-000105", "book-000106"],
    #         "descending": None,
    #     }

    #     result = await hyper.data.list(options)
    #     self.assertEqual(result["ok"], True, "List result not ok.")
    #     self.assertEqual(len(result["docs"]), 2, "Length should be 2")

    # async def test_data_query_limit_10(self):

    #     selector = {"type": "book", "name": {"$eq": "The Lorax 103"}}

    #     options: QueryOptions = {
    #         "fields": None,
    #         "sort": None,
    #         "limit": 10,
    #         "useIndex": None,
    #     }

    #     result = await hyper.data.query(selector, options)

    #     self.assertEqual(result["ok"], True, "Query result not ok.")
    #     self.assertEqual(len(result["docs"]), 1, "Length should be 1")


if __name__ == "__main__":
    asynctest.main()
