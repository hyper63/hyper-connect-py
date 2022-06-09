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


def data_add():

    movie: Dict = {
        "_id": "movie-5000",
        "type": "movie",
        "title": "Back to the Future 2",
        "year": "1987",
    }

    result: IdResult = hyper.data.add(movie)
    print("hyper.data.add result --> ", result)
    # OKIdResult: hyper.data.add result -->  {'_id': 'movie-4000', 'ok': True, 'status': 201}
    # NotOkResult: hyper.data.add result -->  {'ok': False, 'status': 409, 'msg': 'document conflict'}


def data_delete():

    id: str = "movie-5001"
    result: IdResult = hyper.data.remove(id)

    print("hyper.data.remove result --> ", result)
    # hyper.data.remove result -->  {'_id': 'movie-5001', 'ok': True, 'status': 200}


def data_get():

    id: str = "movie-5000"
    result: HyperGetResult = hyper.data.get(id)
    print("hyper.data.get result --> ", result)
    # hyper.data.get result -->  {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1987', 'status': 200}


def data_update():

    book: Dict = {
        "_id": "book-000100",
        "type": "book",
        "name": "The Lorax 100",
        "author": "Dr. Suess",
        "published": "1969",
    }

    result: IdResult = hyper.data.update("book-000100", book)
    print("hyper.data.update result --> ", result)
    # hyper.data.update result -->  {'ok': True, '_id': 'book-000100', 'status': 200}


def list_range():

    options: ListOptions = {
        "startkey": "book-000105",
        "endkey": "book-000106",
    }

    result: IdResult = hyper.data.list(options)
    print("hyper.data.list result --> ", result)
    # hyper.data.list result -->  {'docs': [{'_id': 'book-000105', 'type': 'book', 'name': 'The Lorax 105', 'author': 'Dr. Suess', 'published': '1969'}, {'_id': 'book-000106', 'type': 'book', 'name': 'The Lorax 106', 'author': 'Dr. Suess', 'published': '1969'}], 'ok': True, 'status': 200}


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
        "sort": None,
        "limit": 3,
        "useIndex": None,
    }

    result: HyperDocsResult = hyper.data.query(selector, options)
    print("hyper.data.query result --> ", result)
    # hyper.data.query result -->  {'docs': [{'_id': 'book-000010', 'name': 'The Lorax', 'published': '1959'}, {'_id': 'book-000020', 'name': 'The Lumberjack named Lorax the tree slayer', 'published': '1969'}, {'_id': 'book-000100', 'name': 'The Lorax 100', 'published': '1969'}], 'ok': True, 'status': 200}


def query_index():

    name: str = "_idxauthorpublished"
    fields: List[str] = ["author", "published"]

    indexresult: Result = hyper.data.index(name, fields)

    print("index result --> ", indexresult)
    # index result -->  {'ok': True, 'status': 201}

    selector = {"type": "book", "author": "James A. Michener"}

    options: QueryOptions = {
        "fields": ["author", "published"],
        "sort": [{"author": "DESC"}, {"published": "DESC"}],
        "useIndex": "_idxauthorpublished",
    }

    result: HyperDocsResult = hyper.data.query(selector, options)
    print("hyper.data.query result --> ", result)
    # hyper.data.query result -->  {'docs': [{'author': 'James A. Michener', 'published': '1985'}, {'author': 'James A. Michener', 'published': '1959'}, {'author': 'James A. Michener', 'published': '1947'}], 'ok': True, 'status': 200}


def bulk():
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
            "title": "Butch Cass_idy and the Sundance K_id",
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

    result: HyperDocsResult = hyper.data.bulk(docs)
    print("hyper.data.bulk result --> ", result)
    # hyper.data.bulk result -->  {'results': [{'ok': True, '_id': 'movie-6000'}, {'ok': True, '_id': 'movie-6001'}, {'ok': True, '_id': 'movie-6002'}, {'ok': True, '_id': 'movie-6003'}, {'ok': True, '_id': 'movie-6004'}], 'ok': True, 'status': 201}


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
    # OkResult - hyper.cache.add result -->  {'ok': True, 'status': 201}
    # NotOkResult - hyper.cache.add result -->  {'ok': False, 'status': 409, 'msg': 'Document Conflict'}


def get_cache():
    key = "movie-5000"
    result: HyperGetResult = hyper.cache.get_async(key)
    print("hyper.cache.get_async result --> ", result)
    # hyper.cache.get_async result -->  {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1987', 'status': 200}


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

    hyper.search.update(key, doc)


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
    bulkmoviedocs: List[Dict] = [
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

    result: HyperSearchLoadResult = hyper.search.load(docs=bulkmoviedocs)
    print(" hyper.search.load result -> ", result)
