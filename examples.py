from typing import Dict

from dotenv import dotenv_values

from hyper_connect import connect
from hyper_connect.types import (
    Hyper,
    HyperGetResult,
    HyperSearchLoadResult,
    IdResult,
    ListOptions,
    OkDocsResult,
    QueryOptions,
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


def data_add():

    movie: Dict = {
        "_id": "movie-4000",
        "type": "movie",
        "title": "Back to the Future",
        "year": "1985",
    }

    result: IdResult = hyper.data.add(movie)
    print("hyper.data.add result --> ", result)
    # hyper.data.add result -->  {'id': 'movie-4000', 'ok': True, 'status': 201}


def data_delete():

    id: str = "movie-4000"
    result = hyper.data.remove(id)

    print("hyper.data.remove result --> ", result)
    # hyper.data.remove result -->  {'id': 'movie-4000', 'ok': True, 'status': 200}


def data_get():

    id: str = "movie-105"
    result = hyper.data.get(id)
    print("hyper.data.get result --> ", result)


def data_update():

    book: Dict = {
        "_id": "book-000100",
        "type": "book",
        "name": "The Lorax 100",
        "author": "Dr. Suess",
        "published": "1969",
    }

    result = hyper.data.update("book-000100", book)
    print("hyper.data.update result --> ", result)
    # hyper.data.update result -->  {'ok': True, 'id': 'book-000100', 'status': 200}


def list_range():

    options: ListOptions = {
        "startkey": "book-000105",
        "limit": None,
        "endkey": "book-000106",
        "keys": None,
        "descending": None,
    }

    result = hyper.data.list(options)
    print("hyper.data.list result --> ", result)


def list_keys():

    options: ListOptions = {
        "startkey": None,
        "limit": None,
        "endkey": None,
        "keys": ["book-000105", "book-000106"],
        "descending": None,
    }

    result = hyper.data.list(options)
    print("hyper.data.list result --> ", result)


def query():

    selector = {"type": "book"}

    options: QueryOptions = {
        "fields": ["_id", "name", "published"],
        "limit": 3,
    }

    result = hyper.data.query(selector, options)
    print("hyper.data.query result --> ", result)


def query_index():

    index_result = hyper.data.index(
        "idx_author_published", ["author", "published"]
    )

    print("index_result --> ", index_result)

    selector = {"type": "book", "author": "James A. Michener"}

    options: QueryOptions = {
        "fields": ["author", "published"],
        "sort": [{"author": "DESC"}, {"published": "DESC"}],
        "useIndex": "idx_author_published",
    }

    result = hyper.data.query(selector, options)
    print("hyper.data.query result --> ", result)


############################
#
#   CACHE SERVICE EXAMPLES
#
############################


def add_cache():
    movie: Dict = {
        "_id": "movie-5000",
        "type": "movie",
        "title": "Back to the Future 2",
        "year": "1987",
    }

    result = hyper.cache.add(key="movie-5000", value=movie, ttl="1w")
    print("hyper.cache.add result --> ", result)
    # hyper.cache.add result -->  {'ok': True, 'status': 201}


def remove_cache():
    key = "movie-5000"
    result = hyper.cache.remove(key)
    print("hyper.cache.remove result --> ", result)
    # hyper.cache.remove result -->  {'ok': True, 'status': 200}


def update_cache():
    movie: Dict = {
        "_id": "movie-5000",
        "type": "movie",
        "title": "Back to the Future 2",
        "year": "1988",
    }

    result = hyper.cache.set(key="movie-5000", value=movie, ttl="1w")
    print("hyper.cache.set result --> ", result)
    # hyper.cache.set result -->  {'ok': True, 'status': 200}


def query_cache():
    result = hyper.cache.query(pattern="movie-500*")
    print("hyper.cache.query result --> ", result)
    # hyper.cache.query result -->  {'docs': [{'key': 'movie-5001', 'value': {'_id': 'movie-5001', 'type': 'movie', 'title': 'Back to the Future 3', 'year': '1989'}}, {'key': 'movie-5000', 'value': {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1988'}}], 'ok': True, 'status': 200}


############################
#
#   SEARCH SERVICE EXAMPLES
#
############################


def add_search():
    movie: Dict = {
        "_id": "movie-5000",
        "type": "movie",
        "title": "Back to the Future 2",
        "year": "1987",
    }

    result = hyper.search.add(key="movie-5000", doc=movie)
    print("hyper.search.add result --> ", result)
    # hyper.search.add result -->  {'ok': True, 'status': 201}


def get_search():
    result: HyperGetResult = hyper.search.get(key="movie-5000")
    print("hyper.search.get result --> ", result)
    # hyper.search.get result -->  {'key': 'movie-5000', 'doc': {'type': 'movie', 'title': 'Back to the Future 2', 'year': '1988', '_id': 'movie-5000'}, 'ok': True, 'status': 200}


def remove_search():
    key = "movie-5000"
    result = hyper.search.remove(key)
    print("hyper.search.remove result --> ", result)
    # hyper.search.remove result -->  {'ok': True, 'status': 200}


def update_search():
    movie: Dict = {
        "_id": "movie-5000",
        "type": "movie",
        "title": "Back to the Future 2",
        "year": "1988",
    }

    result = hyper.search.update(key="movie-5000", doc=movie)
    print("hyper.search.update result --> ", result)
    # hyper.search.update result -->  {'ok': True, 'status': 200}


def query_search():

    query: str = "Future"

    options: SearchQueryOptions = {
        "fields": ["_id", "title", "year"],
        "filter": None,
    }
    result = hyper.search.query(query, options)

    print("hyper.search.query result --> ", result)
    # hyper.search.query result -->  {'matches': [{'type': 'movie', 'title': 'Back to the Future', 'year': '1985', '_id': 'movie-102'}], 'ok': True, 'status': 200}


def load_search():
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

    result: HyperSearchLoadResult = hyper.search.load(docs=bulk_movie_docs)
    print(" hyper.search.load result -> ", result)
