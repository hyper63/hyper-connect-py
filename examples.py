from typing import Dict

from dotenv import dotenv_values

from hyper_connect import connect
from hyper_connect.types import Hyper, ListOptions, QueryOptions

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

    result = await hyper.data.add_async(movie)
    print("hyper.data.add result --> ", result)
    # hyper.data.add result -->  {'id': 'movie-4000', 'ok': True, 'status': 201}


async def data_delete():

    id: str = "movie-4000"
    result = await hyper.data.remove(id)

    print("hyper.data.remove result --> ", result)
    # hyper.data.remove result -->  {'id': 'movie-4000', 'ok': True, 'status': 200}


async def data_get():

    id: str = "movie-105"
    result = await hyper.data.get(id)
    print("hyper.data.get result --> ", result)


async def data_update():

    book: Dict = {
        "_id": "book-000100",
        "type": "book",
        "name": "The Lorax 100",
        "author": "Dr. Suess",
        "published": "1969",
    }

    result = await hyper.data.update("book-000100", book)
    print("hyper.data.update result --> ", result)
    # hyper.data.update result -->  {'ok': True, 'id': 'book-000100', 'status': 200}


async def list_range():

    options: ListOptions = {
        "startkey": "book-000105",
        "limit": None,
        "endkey": "book-000106",
        "keys": None,
        "descending": None,
    }

    result = await hyper.data.list(options)
    print("hyper.data.list result --> ", result)


async def list_keys():

    options: ListOptions = {
        "startkey": None,
        "limit": None,
        "endkey": None,
        "keys": ["book-000105", "book-000106"],
        "descending": None,
    }

    result = await hyper.data.list(options)
    print("hyper.data.list result --> ", result)


async def query():

    selector = {"type": "book"}

    options: QueryOptions = {
        "fields": ["_id", "name", "published"],
        "sort": None,
        "limit": 3,
        "useIndex": None,
    }

    result = await hyper.data.query(selector, options)
    print("hyper.data.query result --> ", result)


async def query_index():

    index_result = await hyper.data.index(
        "idx_author_published", ["author", "published"]
    )

    print("index_result --> ", index_result)

    selector = {"type": "book", "author": "James A. Michener"}

    options: QueryOptions = {
        "fields": ["author", "published"],
        "sort": [{"author": "DESC"}, {"published": "DESC"}],
        "useIndex": "idx_author_published",
        "limit": None,
    }

    result = await hyper.data.query(selector, options)
    print("hyper.data.query result --> ", result)
