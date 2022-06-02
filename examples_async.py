from typing import Dict

from dotenv import dotenv_values

from hyper_connect import connect
from hyper_connect.types import Hyper, ListOptions, SearchQueryOptions

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

    result = await hyper.data.add_async(movie)
    print("hyper.data.add_async result --> ", result)
    # hyper.data.add_async result -->  {'id': 'movie-4000', 'ok': True, 'status': 201}


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
    result = await hyper.data.remove_async(id)

    print("hyper.data.remove_async result --> ", result)
    # hyper.data.remove_async result -->  {'id': 'movie-5001', 'ok': True, 'status': 200}


async def data_get():

    id: str = "movie-5000"
    result = await hyper.data.get_async(id)
    print("hyper.data.get result --> ", result)
    # hyper.data.get result -->  {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1987', 'status': 200}


async def data_update():

    book: Dict = {
        "_id": "book-000100",
        "type": "book",
        "name": "The Lorax 100",
        "author": "Dr. Suess",
        "published": "1969",
    }

    result = await hyper.data.update_async("book-000100", book)
    print("hyper.data.update result --> ", result)
    # hyper.data.update_async result -->  {'ok': True, 'id': 'book-000100', 'status': 200}


async def list_range():

    options: ListOptions = {
        "startkey": "book-000105",
        "limit": None,
        "endkey": "book-000106",
        "keys": None,
        "descending": None,
    }

    result = await hyper.data.list_async(options)
    print("hyper.data.list_async result --> ", result)


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

    result = await hyper.data.query_async(selector, options)
    print("hyper.data.query_async result --> ", result)


async def query_index():

    index_result = await hyper.data.index_async(
        "idx_author_published", ["author", "published"]
    )

    print("index_async result --> ", index_result)

    selector = {"type": "book", "author": "James A. Michener"}

    options: QueryOptions = {
        "fields": ["author", "published"],
        "sort": [{"author": "DESC"}, {"published": "DESC"}],
        "useIndex": "idx_author_published",
        "limit": None,
    }

    result = await hyper.data.query_async(selector, options)
    print("hyper.data.query_async result --> ", result)


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

    result = await hyper.cache.add_async(
        key="movie-5000", value=movie, ttl="1w"
    )
    print("hyper.cache.add_async result --> ", result)
    # hyper.cache.add_async result -->  {'ok': True, 'status': 201}


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
    result = await hyper.cache.query_async(pattern="movie-500*")
    print("hyper.cache.query_async result --> ", result)
    # hyper.cache.query_async result -->  {'docs': [{'key': 'movie-5001', 'value': {'_id': 'movie-5001', 'type': 'movie', 'title': 'Back to the Future 3', 'year': '1989'}}, {'key': 'movie-5000', 'value': {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1988'}}], 'ok': True, 'status': 200}

    hyper.search.update(key, doc)


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
