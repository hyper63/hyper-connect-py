# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
import unittest
from typing import Dict, List

from artifacts import movie_bulk_doc_artifacts, movie_doc_artifacts
from dotenv import dotenv_values
from promisio import Promise
from ramda import head, is_empty, map, sum

from hyper_connect import connect
from hyper_connect.types import (
    Hyper,
    HyperGetResult,
    HyperSearchLoadResult,
    HyperSearchQueryResult,
    Result,
    SearchQueryOptions,
)

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


class TestSearchIntegration_SYNC(unittest.TestCase):
    def test_search_add_sync(self):

        remove_result: Result = hyper.search.remove(key=movie1["_id"])
        add_result: Result = hyper.search.add(key=movie1["_id"], doc=movie1)

        self.assertEqual(
            remove_result["ok"], True, "SYNC Removing data doc not ok."
        )
        self.assertEqual(
            add_result["ok"], True, "SYNC Adding data doc not ok."
        )

    def test_search_get_sync(self):
        result: HyperGetResult = hyper.search.get(key="movie-100")

        doc = result["doc"]

        self.assertEqual(
            doc["title"],
            "Chariots of Fire",
            "Getting doc from search not ok.",
        )

    def test_search_delete_sync(self):
        result: Result = hyper.search.remove(key="movie-101")

        self.assertEqual(
            result["ok"],
            True,
            "Deleting from search not ok",
        )

    def test_search_query_sync(self):

        options: SearchQueryOptions = {"fields": ["title"], "filter": None}

        query = "Chariots"
        result: HyperSearchQueryResult = hyper.search.query(query, options)

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

    def test_search_bulk_sync(self):

        result: HyperSearchLoadResult = hyper.search.load(bulk_movie_docs)

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
    unittest.main()
