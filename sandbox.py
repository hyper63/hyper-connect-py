from promisio import Promise
from ramda import has, join, pick_by

from hyper_connect import connect
from hyper_connect.types import Hyper, ListOptions

# >>> from sandbox import data_add, data_get, data_list
# >>> import asyncio
# >>> asyncio.run(data_add('{ "_id":"book-102","type":"book", "name":"Horton hears a who 2","author":"Dr. Suess","published":"1953" }'))
# >>> asyncio.run(data_list())

hyper: Hyper = connect(
    ""
)

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

    # def not_none_value(val, key):
    #     return val is not None

    # tasty_params = pick_by(not_none_value, options)

    # print("tasty_params BEFORE", tasty_params)

    # print(type(tasty_params["keys"]))

    # print(has("keys", tasty_params))

    # if has("keys", tasty_params) and type(tasty_params["keys"]) is list:
    #     print("tasty")
    #     tasty_params["keys"] = join(",", tasty_params["keys"])

    # print("tasty_params AFTER", tasty_params)

    result = await hyper.data.list(options)

    return result
