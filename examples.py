from typing import Dict

from dotenv import dotenv_values

from hyper_connect import connect
from hyper_connect.types import Hyper

config = dotenv_values("./.env")

connection_string: str = str(config["HYPER"])
hyper: Hyper = connect(connection_string)


async def data_add():

    movie: Dict = {
        "_id": "movie-4000",
        "type": "movie",
        "title": "Back to the Future",
        "year": "1985",
    }

    result = await hyper.data.add(movie)

    print("hyper.data.add result --> ", result)
    # hyper.data.add result -->  {'id': 'movie-4000', 'ok': True, 'status': 201}


async def data_delete():

    id: str = "movie-4000"
    result = await hyper.data.remove(id)
    print("hyper.data.remove result --> ", result)
    # hyper.data.remove result -->  {'id': 'movie-4000', 'ok': True, 'status': 200}
