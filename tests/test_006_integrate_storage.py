# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
import json
from typing import Dict, List

import asynctest
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


if is_empty(config):
    print(
        "You seem to be missing a .env file with a `HYPER` environment variable.  Set HYPER with a connection string from your hyper app keys. https://docs.hyper.io/app-key."
    )
    exit()
else:
    connection_string: str = str(config["HYPER"])

hyper: Hyper = connect(connection_string)


class TestStorageIntegration(asynctest.TestCase):
    async def test_storage_upload(self):

        br: io.BufferedReader = open("test.txt", "rb")

        result = await hyper.storage.upload(name="remix", data=br)

        print("result:", result)

        self.assertEqual(
            True,
            True,
            "Storage upload no es bueno",
        )

    # async def test_search_delete(self):
    #     result = await hyper.search.remove(key="movie-101")

    #     self.assertEqual(
    #         result["ok"],
    #         True,
    #         "Deleting from search not ok",
    #     )


if __name__ == "__main__":
    asynctest.main()
