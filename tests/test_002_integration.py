# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
import json
from typing import Any, Dict, List, Optional

import asynctest
from artifacts import book_doc_artifact
from dotenv import dotenv_values
from promisio import Promise
from ramda import compose, has, head, is_empty, join, merge, pick_by, prop, prop_or

from hyper_connect import connect
from hyper_connect.types import Hyper, ListOptions, QueryOptions

# import requi9red module
# import sys
# sys.path.append("..")
# append the path of the
# parent directory


config = dotenv_values("./.env")

book_doc: Dict = book_doc_artifact()


if is_empty(config):
    print(
        "You seem to be missing a .env file with a `HYPER` environment variable.  Set HYPER with a connection string from your hyper app keys. https://docs.hyper.io/app-key."
    )
    exit()
else:
    connection_string: str = str(config["HYPER"])

hyper: Hyper = connect(connection_string)


class TestIntegration(asynctest.TestCase):
    async def test_data_get(self):

        result = await hyper.data.remove(book_doc["_id"]).then(
            lambda x: hyper.data.add(book_doc)
        )

        self.assertEqual(result["ok"], True, "Adding doc not ok.")


if __name__ == "__main__":
    asynctest.main()
