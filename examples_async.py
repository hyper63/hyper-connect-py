from typing import Dict

from dotenv import dotenv_values

from hyper_connect import connect
from hyper_connect.types import (
    Hyper,
    HyperDocsResult,
    HyperGetResult,
    IdResult,
    ListOptions,
    OkIdResult,
    QueryOptions,
    Result,
    SearchQueryOptions,
)

config = dotenv_values("./.env")

connection_string: str = str(config["HYPER"])
hyper: Hyper = connect(connection_string)

############################
#
#   DATA SERVICE EXAMPLES
#
############################


async def data_add():

    movie: Dict = {
        "_id": "movie-5000",
        "type": "movie",
        "title": "Back to the Future 2",
        "year": "1987",
    }

    result: IdResult = await hyper.data.add_async(movie)
    print("hyper.data.add_async result --> ", result)
    # OKIdResult: hyper.data.add_async result -->  {'id': 'movie-4000', 'ok': True, 'status': 201}
    # NotOkResult: hyper.data.add_async result -->  {'ok': False, 'status': 409, 'msg': 'document conflict'}


async def data_cache_compose():
    movie: Dict = {
        "_id": "movie-5001",
        "type": "movie",
        "title": "Back to the Future 3",
        "year": "1989",
    }

    result = await hyper.data.add_async(movie).then(
        lambda _: hyper.cache.add_async(
            key=movie["_id"], value=movie, ttl="1d"
        )
    )
    print("hyper data and cache add_async result --> ", result)


async def data_delete():

    id: str = "movie-5001"
    result: IdResult = await hyper.data.remove_async(id)

    print("hyper.data.remove_async result --> ", result)
    # hyper.data.remove_async result -->  {'id': 'movie-5001', 'ok': True, 'status': 200}


async def data_get():

    id: str = "movie-5000"
    result: HyperGetResult = await hyper.data.get_async(id)
    print("hyper.data.get_async result --> ", result)
    # hyper.data.get_async result -->  {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1987', 'status': 200}


async def data_update():

    book: Dict = {
        "_id": "book-000100",
        "type": "book",
        "name": "The Lorax 100",
        "author": "Dr. Suess",
        "published": "1969",
    }

    result: IdResult = await hyper.data.update_async("book-000100", book)
    print("hyper.data.update_async result --> ", result)
    # hyper.data.update_async result -->  {'ok': True, 'id': 'book-000100', 'status': 200}


async def list_range():

    options: ListOptions = {
        "startkey": "book-000105",
        "endkey": "book-000106",
    }

    result: IdResult = await hyper.data.list_async(options)
    print("hyper.data.list_async result --> ", result)
    # hyper.data.list_async result -->  {'docs': [{'_id': 'book-000105', 'type': 'book', 'name': 'The Lorax 105', 'author': 'Dr. Suess', 'published': '1969'}, {'_id': 'book-000106', 'type': 'book', 'name': 'The Lorax 106', 'author': 'Dr. Suess', 'published': '1969'}], 'ok': True, 'status': 200}


async def list_keys():

    options: ListOptions = {
        "startkey": None,
        "limit": None,
        "endkey": None,
        "keys": ["book-000105", "book-000106"],
        "descending": None,
    }

    result = await hyper.data.list_async(options)
    print("hyper.data.list_async result --> ", result)


async def query():

    selector = {"type": "book"}

    options: QueryOptions = {
        "fields": ["_id", "name", "published"],
        "sort": None,
        "limit": 3,
        "useIndex": None,
    }

    result: HyperDocsResult = await hyper.data.query_async(selector, options)
    print("hyper.data.query_async result --> ", result)
    # hyper.data.query_async result -->  {'docs': [{'_id': 'book-000010', 'name': 'The Lorax', 'published': '1959'}, {'_id': 'book-000020', 'name': 'The Lumberjack named Lorax the tree slayer', 'published': '1969'}, {'_id': 'book-000100', 'name': 'The Lorax 100', 'published': '1969'}], 'ok': True, 'status': 200}


async def query_index():

    name: str = "idx_author_published"
    fields: List[str] = ["author", "published"]

    index_result: Result = await hyper.data.index_async(name, fields)

    print("index_async result --> ", index_result)
    # index_async result -->  {'ok': True, 'status': 201}

    selector = {"type": "book", "author": "James A. Michener"}

    options: QueryOptions = {
        "fields": ["author", "published"],
        "sort": [{"author": "DESC"}, {"published": "DESC"}],
        "useIndex": "idx_author_published",
    }

    result: HyperDocsResult = await hyper.data.query_async(selector, options)
    print("hyper.data.query_async result --> ", result)
    # hyper.data.query_async result -->  {'docs': [{'author': 'James A. Michener', 'published': '1985'}, {'author': 'James A. Michener', 'published': '1959'}, {'author': 'James A. Michener', 'published': '1947'}], 'ok': True, 'status': 200}


async def bulk():
    docs: list[Dict] = [
        {
            "_id": "movie-6000",
            "type": "movie",
            "title": "Jeremiah Johnson",
            "year": "1972",
        },
        {
            "_id": "movie-6001",
            "type": "movie",
            "title": "Butch Cassidy and the Sundance Kid",
            "year": "1969",
        },
        {
            "_id": "movie-6002",
            "type": "movie",
            "title": "The Great Gatsby",
            "year": "1974",
        },
        {
            "_id": "movie-6003",
            "type": "movie",
            "title": "The Natural",
            "year": "1984",
        },
        {
            "_id": "movie-6004",
            "type": "movie",
            "title": "The Sting",
            "year": "1973",
        },
    ]

    result: HyperDocsResult = await hyper.data.bulk_async(docs)
    print("hyper.data.bulk_async result --> ", result)
    # hyper.data.bulk_async result -->  {'results': [{'ok': True, 'id': 'movie-6000'}, {'ok': True, 'id': 'movie-6001'}, {'ok': True, 'id': 'movie-6002'}, {'ok': True, 'id': 'movie-6003'}, {'ok': True, 'id': 'movie-6004'}], 'ok': True, 'status': 201}


############################
#
#   CACHE SERVICE EXAMPLES
#
############################


async def add_cache():
    movie: Dict = {
        "_id": "movie-5000",
        "type": "movie",
        "title": "Back to the Future 2",
        "year": "1987",
    }

    result: Result = await hyper.cache.add_async(
        key="movie-5000", value=movie, ttl="24h"
    )
    print("hyper.cache.add_async result --> ", result)
    # OkResult - hyper.cache.add result -->  {'ok': True, 'status': 201}
    # NotOkResult - hyper.cache.add result -->  {'ok': False, 'status': 409, 'msg': 'Document Conflict'}


async def add_cache_thing():
    thing: Dict = {"likes": 100}

    result: Result = await hyper.cache.add_async(
        key="thing-1", value=thing, ttl="1m"
    )
    print("hyper.cache.add_async result --> ", result)
    # OkResult - hyper.cache.add result -->  {'ok': True, 'status': 201}
    # NotOkResult - hyper.cache.add result -->  {'ok': False, 'status': 409, 'msg': 'Document Conflict'}


async def get_cache():
    key = "movie-5000"
    result: HyperGetResult = await hyper.cache.get_async(key)
    print("hyper.cache.get_async result --> ", result)
    # hyper.cache.get_async result -->  {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1987', 'status': 200}


async def get_cache_thing():
    key: str = "thing-1"
    result: HyperGetResult = await hyper.cache.get_async(key)
    print("hyper.cache.get_async result --> ", result)
    # hyper.cache.get_async result -->  {'likes': 100, 'status': 200}


async def remove_cache():
    key = "movie-5000"
    result = await hyper.cache.remove_async(key)
    print("hyper.cache.remove_async result --> ", result)
    # hyper.cache.remove_async result -->  {'ok': True, 'status': 200}


async def update_cache():
    movie: Dict = {
        "_id": "movie-5000",
        "type": "movie",
        "title": "Back to the Future 2",
        "year": "1988",
    }

    result = await hyper.cache.set_async(
        key="movie-5000", value=movie, ttl="1w"
    )
    print("hyper.cache.set_async result --> ", result)
    # hyper.cache.set_async result -->  {'ok': True, 'status': 200}


async def query_cache():
    result: HyperDocsResult = await hyper.cache.query_async(
        pattern="movie-500*"
    )
    print("hyper.cache.query_async result --> ", result)
    # hyper.cache.query_async result -->  {'docs': [{'key': 'movie-5001', 'value': {'_id': 'movie-5001', 'type': 'movie', 'title': 'Back to the Future 3', 'year': '1989'}}, {'key': 'movie-5000', 'value': {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1988'}}], 'ok': True, 'status': 200}


############################
#
#   SEARCH SERVICE EXAMPLES
#
############################


async def add_search():
    movie: Dict = {
        "_id": "movie-5000",
        "type": "movie",
        "title": "Back to the Future 2",
        "year": "1987",
    }

    result = await hyper.search.add_async(key="movie-5000", doc=movie)
    print("hyper.search.add_async result --> ", result)
    # hyper.search.add_async result -->  {'ok': True, 'status': 201}


async def get_search():
    result: HyperGetResult = await hyper.search.get_async(key="movie-5000")
    print("hyper.search.get_async result --> ", result)
    # hyper.search.get_async result -->  {'key': 'movie-5000', 'doc': {'type': 'movie', 'title': 'Back to the Future 2', 'year': '1988', '_id': 'movie-5000'}, 'ok': True, 'status': 200}


async def remove_search():
    key = "movie-5000"
    result = await hyper.search.remove_async(key)
    print("hyper.search.remove_async result --> ", result)
    # hyper.search.remove_async result -->  {'ok': True, 'status': 200}


async def update_search():
    movie: Dict = {
        "_id": "movie-5000",
        "type": "movie",
        "title": "Back to the Future 2",
        "year": "1988",
    }

    result = await hyper.search.update_async(key="movie-5000", doc=movie)
    print("hyper.search.update_async result --> ", result)
    # hyper.search.update_async result -->  {'ok': True, 'status': 200}


async def query_search():

    query: str = "Future"

    options: SearchQueryOptions = {
        "fields": ["_id", "title", "year"],
        "filter": None,
    }
    result = await hyper.search.query_async(query, options)

    print("hyper.search.query_async result --> ", result)
    # hyper.search.query_async result -->  {'matches': [{'type': 'movie', 'title': 'Back to the Future', 'year': '1985', '_id': 'movie-102'}], 'ok': True, 'status': 200}


async def load_search():
    bulk_movie_docs: List[Dict] = [
        {
            "_id": "movie-104",
            "type": "movie",
            "title": "Full Metal Jacket",
            "year": "1987",
        },
        {
            "_id": "movie-105",
            "type": "movie",
            "title": "Predator",
            "year": "1987",
        },
    ]

    result: HyperSearchLoadResult = await hyper.search.load_async(
        docs=bulk_movie_docs
    )
    print(" hyper.search.load_async result -> ", result)
