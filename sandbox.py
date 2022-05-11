from dotenv import dotenv_values
from promisio import Promise
from ramda import has, join, pick_by

from hyper_connect import connect
from hyper_connect.types import Hyper, ListOptions

config = dotenv_values(".env")

# >>> from sandbox import data_add, data_get, data_list
# >>> import asyncio
# >>> asyncio.run(data_add('{ "_id":"book-102","type":"book", "name":"Horton hears a who 2","author":"Dr. Suess","published":"1953" }'))
# >>> asyncio.run(data_list())

hyper: Hyper = connect(config["HYPER"])

# passValueThru = lambda x: x


def error_response(err):
    print("sandbox error_response!! err", err)
    response = {"ok": False, "err": err}
    return response


async def data_add(doc: str):

    result = await hyper.data.add(doc).catch(error_response)

    return result


async def data_get(id: str):

    result = await hyper.data.get(id)

    return result


async def data_list():

    # options: ListOptions = {
    #     "startkey": "movie-5",
    #     "limit": None,
    #     "endkey": None,
    #     "keys": None,
    #     "descending": None,
    # }

    # options: ListOptions = {
    #     "startkey": "movie-5",
    #     "limit": None,
    #     "endkey": "movie-7",
    #     "keys": None,
    #     "descending": None,
    # }

    options: ListOptions = {
        "startkey": None,
        "limit": None,
        "endkey": None,
        "keys": ["movie-1", "movie-11"],
        "descending": None,
    }

    result = await hyper.data.list(options)

    return result
