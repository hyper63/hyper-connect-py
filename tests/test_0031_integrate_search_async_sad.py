# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
from typing import Dict, List

import asynctest
from artifacts import movie_bulk_doc_artifacts, movie_doc_artifacts
from dotenv import dotenv_values
from ramda import head, is_empty

from hyper_connect import connect
from hyper_connect.types import Hyper, NotOkResult

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


class TestSearchIntegration_ASYNC_SAD(asynctest.TestCase):
    async def test_search_add_duplicate_async_sad(self):

        duplicate_doc: Dict = {
            "_id": "movie-100",
            "type": "movie",
            "title": "Chariots of Fire",
            "year": "1981",
        }

        result: NotOkResult = await hyper.search.add_async(
            key=duplicate_doc["_id"], doc=duplicate_doc
        )

        self.assertEqual(
            result["status"], 409, "Duplicate error did not occur."
        )

    async def test_search_get_missing_async_sad(self):
        result: NotOkResult = await hyper.search.get_async(key="xyz-123")

        status = result["status"]

        self.assertEqual(
            status,
            404,
            "404 error did not occur",
        )


if __name__ == "__main__":
    asynctest.main()
