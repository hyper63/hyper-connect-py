# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
import json
import os
import shutil
import sys
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
    async def test_storage_image_upload(self):

        br: io.BufferedReader = open(
            os.path.join(sys.path[0], "remix.png"), "rb"
        )
        result = await hyper.storage.upload(name="remix", data=br).then(
            lambda _: hyper.storage.download(name="remix")
        )

        br.close()

        path = os.path.join(sys.path[0], "remix_downloaded.png")

        with open(path, "wb") as fd:
            for chunk in result.iter_content(chunk_size=128):
                fd.write(chunk)

        self.assertEqual(
            result.status_code,
            200,
            "Storage download status isn't 200. no es bueno",
        )

    async def test_storage_delete(self):
        result = await hyper.storage.remove(name="remix")

        print("storage delete result", result)

        self.assertEqual(
            result["ok"],
            True,
            "Deleting from search not ok",
        )


if __name__ == "__main__":
    asynctest.main()
