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


class TestInfoIntegeration(asynctest.TestCase):
    async def test_get_info_services(self):
        result = await hyper.info.services()

        # result --> {'name': 'hyper', 'version': '1.0-beta', 'services': ['cache', 'data', 'storage', 'search', 'queue'], 'status': 200}

        self.assertEqual(
            result["status"],
            200,
            "The status isn't 200.  No es bueno!",
        )

        self.assertEqual(
            result["name"],
            "hyper",
            "The name isn't 'hyper'.  No es bueno!",
        )


if __name__ == "__main__":
    asynctest.main()
