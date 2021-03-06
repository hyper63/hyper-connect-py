# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v
import os
import sys
import unittest

from dotenv import dotenv_values
from ramda import is_empty

from hyper_connect import connect
from hyper_connect.types import Hyper

config = dotenv_values("./.env")


if is_empty(config):
    print(
        "You seem to be missing a .env file with a `HYPER` environment variable.  Set HYPER with a connection string from your hyper app keys. https://docs.hyper.io/app-key."
    )
    exit()
else:
    connection_string: str = str(config["HYPER"])

hyper: Hyper = connect(connection_string)


class TestStorageIntegrationTXT_SYNC(unittest.TestCase):
    def test_storage_image_upload_sync(self):

        # begin upload remix.png image file
        br_hyper_txt: io.BufferedReader = open(
            os.path.join(sys.path[0], "hyper.txt"), "rb"
        )

        br_remix_txt_upload_result = hyper.storage.upload(
            name="hyper.txt", data=br_hyper_txt
        )

        br_hyper_txt_download_result = hyper.storage.download(name="hyper.txt")

        br_hyper_txt.close()
        # end upload

        # begin download of remix.png image file as remix_downloaded.png
        path = os.path.join(sys.path[0], "hyper_downloaded.txt")

        with open(path, "wb") as fd:
            for chunk in br_hyper_txt_download_result.iter_content(
                chunk_size=128
            ):
                fd.write(chunk)

        # end download

        self.assertEqual(
            br_hyper_txt_download_result.status_code,
            200,
            "Storage download status isn't 200. no es bueno",
        )

        remove_result = hyper.storage.remove(name="hyper.txt")

        self.assertEqual(
            remove_result["ok"],
            True,
            "Deleting hyper.txt from storage not ok",
        )


if __name__ == "__main__":
    unittest.main()
