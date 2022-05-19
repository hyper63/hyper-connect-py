# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
import json
from typing import Dict, List

import asynctest
from artifacts import movie_bulk_doc_artifacts, movie_doc_artifacts
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
from hyper_connect.types import Hyper, ListOptions, SearchQueryOptions

config = dotenv_values("./.env")

movie_docs: List[Dict] = movie_doc_artifacts()

bulk_movie_docs: List[Dict] = movie_bulk_doc_artifacts()

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
        result = await hyper.search.get(key="movie-100")

        doc = result["doc"]

        self.assertEqual(
            doc["title"],
            "Chariots of Fire",
            "Getting doc from search not ok.",
        )

    async def test_search_delete(self):
        result = await hyper.search.remove(key="movie-101")

        self.assertEqual(
            result["ok"],
            True,
            "Deleting from search not ok",
        )

    async def test_search_query(self):

        options: SearchQueryOptions = {"fields": ["title"], "filter": None}

        query = "Chariots"
        result = await hyper.search.query(query, options)

        self.assertEqual(
            result["ok"],
            True,
            "Deleting from search not ok",
        )

        self.assertEqual(
            len(result["matches"]),
            1,
            "# of search result matches do not equal 1.",
        )

    async def test_search_bulk(self):

        result = await hyper.search.load(bulk_movie_docs)

        print("test_search_bulk result:", result)

        # {"ok": True, "results": []}

        self.assertEqual(
            result["ok"],
            True,
            "Bulk load to search not ok",
        )

        self.assertEqual(
            len(result["results"]),
            2,
            "# of bulk search load results does not equal 2.",
        )


if __name__ == "__main__":
    asynctest.main()
