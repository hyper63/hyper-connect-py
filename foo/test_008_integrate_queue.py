# Once you have multiple test files, as long as you follow the test*.py naming pattern,
# you can provide the name of the directory instead by using the -s flag and the name of the directory:
# python -m unittest discover -s tests -v

import asynctest
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


class TestQueueIntegeration(asynctest.TestCase):
    async def test_queue_enqueue(self):
        result = await hyper.queue.enqueue(
            {"type": "NEW_MOVIE", "id": "movie-1"}
        )
        self.assertEqual(
            result["status"], 201, "enqueue a job isn't 201. no es bueno!"
        )


if __name__ == "__main__":
    asynctest.main()
