import io
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Literal,
    Optional,
    TypedDict,
    Union,
)

import requests

SortOptions = Literal["DESC", "ASC"]
ServiceType = Literal["data", "cache", "storage", "search", "queue", "info"]
Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
Action = Literal["_query", "_bulk", "_index"]
QueueStatus = Literal["ERROR", "READY"]


class OkResult:
    """
    A class to represent a successful result.

    ...

    Attributes
    ----------
    ok : bool
        Value will be True
    status : int
        HTTP status code.
    """

    ok: ClassVar[bool] = True
    status: int


class NotOkResult:
    """
    A class to represent an error.

    ...

    Attributes
    ----------
    ok : bool
        Value will be False
    status : int
        HTTP status code.
    msg : str
        Error message.
    """

    ok: ClassVar[bool] = False
    status: int
    msg: str


{"id": "movie-4000", "ok": True, "status": 201}


class OkIdResult:
    """
    A class to represent a successful result along with the id of the resource.
    Example:  After adding a document to the hyper data service,
    the result will look similar to:

        {'id': 'movie-4000', 'ok': True, 'status': 201}
    ...

    Attributes
    ----------
    ok : bool
        Value will be True
    status : int
        HTTP status code
    id : int
        resource identifier
    """

    ok: ClassVar[bool] = True
    status: int
    id: str


class OkDocsResult:
    """
    A class to represent a successful result along with the returned docs.

    ...

    Attributes
    ----------
    ok : bool
        Value will be True
    status : int
        HTTP status code
    docs : List[Dict]
        list of documents
    """

    ok: ClassVar[bool] = True
    status: int
    docs: List[Dict]


class NotOkDocsResult:
    """
    A class to represent a unsuccessful result along with an empty list of documents.

    ...

    Attributes
    ----------
    ok : bool
        Value will be False
    status : int
        HTTP status code
    msg : str
        Error message
    docs : List[Dict]
        empty list of documents
    """

    ok: ClassVar[bool] = False
    status: int
    msg: str
    docs: List[Dict]


IdResult = Union[OkIdResult, NotOkResult]

Result = Union[OkResult, NotOkResult]

HyperGetResult = Union[Dict, NotOkResult]

HyperDocsResult = Union[OkDocsResult, NotOkDocsResult]


class HyperSearchQueryOKResult:
    """
    A class to represent a successful search query result along with the returned docs.

    ...

    Attributes
    ----------
    ok : bool
        Value will be True
    status : int
        HTTP status code
    matches : List[Dict]
        list of matched documents
    """

    ok: ClassVar[bool] = True
    status: int
    matches: List[Dict]


class HyperSearchLoadOKResult:
    """
    A class to represent a successful search bulk load result along with the returned docs.

    ...

    Attributes
    ----------
    ok : bool
        Value will be True
    status : int
        HTTP status code
    results : List[Dict]
        list of bulk load result documents
    """

    ok: ClassVar[bool] = True
    status: int
    results: List[Dict]


HyperSearchQueryResult = Union[HyperSearchQueryOKResult, NotOkResult]

HyperSearchLoadResult = Union[HyperSearchLoadOKResult, NotOkResult]


class ListOptions(TypedDict, total=False):
    """
    data list options.

    Some keys are optional and may set to None or simply omit the key.

    Example: both of the following typed Dictionaries are valid:

        valid_data_list_options: ListOptions = {
            "startkey": "book-000105",
            "limit": None,
            "endkey": "book-000106",
            "keys": None,
            "descending": None,
        }

        also_valid_options: ListOptions = {
            "startkey": "book-000105",
            "endkey": "book-000106"
        }

    Example: List a range of docs:

        options: ListOptions = {
            "startkey": "book-000105",
            "limit": None,
            "endkey": "book-000106",
            "keys": None,
            "descending": None,
        }

        result = hyper.data.list(options)

    Example: List a set of docs:

        options: ListOptions = {
            "startkey": None,
            "limit": None,
            "endkey": None,
            "keys": ["book-000105", "book-000106"],
            "descending": None,
        }

        result = hyper.data.list(options)
    ...

    Attributes
    ----------
    limit : int, optional
        default: 1000  - limits the number of documents returned
    startkey : str, optional
        key matcher for document id's.  May use with endkey to return a range of documents.
    endkey : str, optional
        key matcher for document id's
    keys: List[str], optional
        a comma delimited list of key ids for returning documents. Ex: '"keys": ["book-000105", "book-000106"]'
    descending: bool, optional
        determines the order of the list sorted on the 'id' column
    """

    limit: Optional[int]
    startkey: Optional[str]
    endkey: Optional[str]
    keys: Optional[List[str]]
    descending: Optional[bool]


class QueryOptions(TypedDict, total=False):
    """
    data service query options for hyper.data.query().

    Example: Fields and limit query options:

        selector = {"type": "book"}

        options: QueryOptions = {
            "fields": ["_id", "name", "published"],
            "limit": 3
        }

        result = hyper.data.query(selector, options)

    Example: Creates an index with fields, sort, and useIndex query option:

        index_result = hyper.data.index(
            "idx_author_published", ["author", "published"]
        )

        print("index_result --> ", index_result)

        selector = {"type": "book", "author": "James A. Michener"}

        options: QueryOptions = {
            "fields": ["author", "published"],
            "sort": [{"author": "DESC"}, {"published": "DESC"}],
            "useIndex": "idx_author_published"
        }

        result = hyper.data.query(selector, options)

    ...

    Attributes
    ----------
    fields : List[str], optional
        A list of keys/properties to return from the query.
        Valuable for large documents with many keys.
        Similar to a SQL SELECT clause.
    sort : List[Dict[str, SortOptions]], optional
        The order you would like your results returned
    limit : int, optional
        limits the number of documents returned.
    useIndex : str, optional
        name of the index to use for this query.
        Indexes are used to provide fast search when querying a data service.
        See: https://docs.hyper.io/create-an-index and
        the index and index_async methods on the hyper data service.
    """

    fields: Optional[List[str]]
    sort: Optional[List[Dict[str, SortOptions]]]
    limit: Optional[int]
    useIndex: Optional[str]


class SearchQueryOptions(TypedDict, total=False):
    """
    Options used when querying the search index

        Example:

        options: SearchQueryOptions = {"fields": ["title"], "filter": None}

        query = "Chariots"
        result: HyperSearchQueryResult = hyper.search.query(query, options)
    ...

    Attributes
    ----------
    fields : List[str], optional
        a list of fields you would like to target the search against
    filter : Dict[str, str], optional
        key/value pairs to filter the search results

    """

    fields: Optional[List[str]]
    filter: Optional[Dict[str, str]]


class HyperRequest(TypedDict):
    service: ServiceType
    method: Method
    resource: Optional[str]
    body: Any
    params: Union[ListOptions, QueryOptions, Dict[str, str], None]
    action: Optional[Action]


class RequestOptions(TypedDict):
    headers: Dict[str, str]
    method: Method
    body: Any


# Example HyperRequestParams
# {
#     'url': 'https://cloud.hyper.io/express-quickstart/data/default',
#     'options': {
#         'headers': {
#             'Content-Type': 'application/json',
#             'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ4bWd0YTBudW02ajduNnVuN2FhNm91Z2EyNnZxbjc4NCIsImV4cCI6MTY1MTc2NTAwMX0.ChZqjXFOJDYFgsHMFHLTk_iIRR-qW1BfRutJxMObvqE'
#             },
#         'method': 'GET',
#         'body': 'foo bar'
#     }
# }


class HyperRequestParams(TypedDict):
    url: str
    options: RequestOptions


# HyperData Classes
class WriteHyperDataError(Exception):
    pass


class HyperCache:
    """
    The cache service improves the performance of your applications by allowing you to retrieve information from fast,
    managed, in-memory data stores, instead of relying entirely on slower disk-based databases.
    A hyper Cache service is a key-value store.
    The key is a unique string and the value is a document.
    This service keeps caching simple giving you a pattern matcher query to return a filtered set of values, or you can retrieve directly by key.
    See: https://docs.hyper.io/cache-api

    ...
    Methods
    -------
    add(key, value, ttl):
        Creates a cached key, value pair in the cache service.
    remove(key):
        Deletes the key/value pair from the cache service.
    get(key):
        Returns a specific value cached for the specified key.
    set(key, value, ttl):
        Updates a document in the cache service.
    query(selector, options)
        Query using a comparion pattern.
        When applied the pattern will be used to match all the keys
        in the cache and only return the ones that match the pattern.
        Using the * wildcard, you can define patterns like "movie*" that
        match all the key values that either start with the provided pattern,
        end with the pattern, or is in-between the pattern.
        Examples:
            - starts with "movie*"
            - ends with "*-1984"
            - in-bewteen "movie*1984"


    add_async(key, value, ttl):
        Asynchronously creates a cached key, value pair in the cache service.
    remove_async(key):
        Asynchronously deletes the key/value pair from the cache service.
    get_async(key):
        Asynchronously returns a specific value cached for the specified key.
    set_async(key, value, ttl):
        Asynchronously updates a document in the cache service.
    query_async(selector, options)
        Asynchronously query using a comparion pattern.
        When applied the pattern will be used to match all the keys
        in the cache and only return the ones that match the pattern.
        Using the * wildcard, you can define patterns like "movie*" that
        match all the key values that either start with the provided pattern,
        end with the pattern, or is in-between the pattern.
        Examples:
            - starts with "movie*"
            - ends with "*-1984"
            - in-bewteen "movie*1984"
    """

    def __init__(
        self,
        # ASYNC
        add_cache_async_fn: Callable,
        get_cache_async_fn: Callable,
        set_cache_async_fn: Callable,
        remove_cache_async_fn: Callable,
        post_cache_query_async_fn: Callable,
        # SYNC
        add_cache_sync_fn: Callable,
        get_cache_sync_fn: Callable,
        set_cache_sync_fn: Callable,
        remove_cache_sync_fn: Callable,
        post_cache_query_sync_fn: Callable,
    ):
        # ASYNC
        self._add_cache_async = add_cache_async_fn
        self._get_cache_async = get_cache_async_fn
        self._set_cache_async = set_cache_async_fn
        self._remove_cache_async = remove_cache_async_fn
        self._post_cache_query_async = post_cache_query_async_fn

        # SYNC
        self._add_cache_sync = add_cache_sync_fn
        self._get_cache_sync = get_cache_sync_fn
        self._set_cache_sync = set_cache_sync_fn
        self._remove_cache_sync = remove_cache_sync_fn
        self._post_cache_query_sync = post_cache_query_sync_fn

    # ASYNC
    def add_async(self, key: str, value: Dict, ttl: Optional[str]) -> Result:
        """
        Asynchronously creates a cached key, value pair in the cache service.
        ou can also specify the time to live property on this request which
        will specify how long you wish the document to be in the cache.

        Example:

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

        Parameters
        ----------
        key : str
            - must begin with lowercase letter (`a-z`)
            - must be lowercase letters (`a-z`)
            - digits (`0-9`)
            - any of these characters `_ $ + -`

        value: Dict
            The dictionary you wish to cache.
        ttl: str, optional
            instructs cache on how long the key/pair should remain in the cache
                 - `s` seconds. eg: 20s = 20 seconds
                - `m` minutes. eg: 10m = 10 minutes
                - `h` hours. ex: 12h = 12 hours
                - `d` days. ex: 14d = 14 days
                - `w` weeks. ex: 1w = 1 week

        Returns
        -------
        Promise of a Result.
        """
        return self._add_cache_async(key, value, ttl)

    def get_async(self, key: str) -> HyperGetResult:
        """
        Asynchronously returns a specific value cached for the specified key.

        Example:
            key = "movie-5000"
            result: HyperGetResult = await hyper.cache.get_async(key)
            print("hyper.cache.get_async result --> ", result)
            # hyper.cache.get_async result -->  {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1987', 'status': 200}


        Parameters
        ----------
        key : str
            - must begin with lowercase letter (`a-z`)
            - must be lowercase letters (`a-z`)
            - digits (`0-9`)
            - any of these characters `_ $ + -`

        Returns
        -------
        Promise of a HyperGetResult.
        """
        return self._get_cache_async(key)

    def set_async(self, key: str, value: Dict, ttl: Optional[str]) -> Result:
        """
        Asynchronously updates a document in the cache store.
        By updating the document you can modify the values of the document,
        as well as modify/extend the time to live or ttl.

        Example:

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


        Parameters
        ----------
        key : str
            - must begin with lowercase letter (`a-z`)
            - must be lowercase letters (`a-z`)
            - digits (`0-9`)
            - any of these characters `_ $ + -`

        value: Dict
            The dictionary you wish to update within the cache.
        ttl: str, optional
            instructs cache on how long the key/pair should remain in the cache
                - `s` seconds. eg: 20s = 20 seconds
                - `m` minutes. eg: 10m = 10 minutes
                - `h` hours. ex: 12h = 12 hours
                - `d` days. ex: 14d = 14 days
                - `w` weeks. ex: 1w = 1 week

        Returns
        -------
        Promise of a Result.
        """

        return self._set_cache_async(key, value, ttl)

    def remove_async(self, key: str) -> Result:
        """
        Asynchronously deletes the key/value pair from the cache store.

        Example:

            key = "movie-5000"
            result = await hyper.cache.remove_async(key)
            print("hyper.cache.remove_async result --> ", result)
             # hyper.cache.remove_async result -->  {'ok': True, 'status': 200}


        Parameters
        ----------
        key : str
            - must begin with lowercase letter (`a-z`)
            - must be lowercase letters (`a-z`)
            - digits (`0-9`)
            - any of these characters `_ $ + -`

        Returns
        -------
        Promise of a Result.
        """
        return self._remove_cache_async(key)

    def query_async(self, pattern: str) -> HyperDocsResult:
        """
        Asynchronously query using a comparion pattern.
        When applied the pattern will be used to match all the keys
        in the cache and only return the ones that match the pattern.
        Using the * wildcard, you can define patterns like "movie*" that
        match all the key values that either start with the provided pattern,
        end with the pattern, or is in-between the pattern.
        Examples:
            - starts with "movie*"
            - ends with "*-1984"
            - in-bewteen "movie*1984"

        Example:
            result : HyperDocsResult = await hyper.cache.query_async(pattern="movie-500*")
            print("hyper.cache.query_async result --> ", result)
             # hyper.cache.query_async result -->  {'docs': [{'key': 'movie-5001', 'value': {'_id': 'movie-5001', 'type': 'movie', 'title': 'Back to the Future 3', 'year': '1989'}}, {'key': 'movie-5000', 'value': {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1988'}}], 'ok': True, 'status': 200}

        Parameters
        ----------
        pattern : str


        Returns
        -------
        Promise of a HyperDocsResult.
        """
        return self._post_cache_query_async(pattern)

    # SYNC
    def add(self, key: str, value: Dict, ttl: Optional[str]) -> Result:
        """
        Creates a cached key, value pair in the cache service.
        ou can also specify the time to live property on this request which
        will specify how long you wish the document to be in the cache.

        Example:

            movie: Dict = {
                "_id": "movie-5000",
                "type": "movie",
                "title": "Back to the Future 2",
                "year": "1987",
            }

            result = hyper.cache.add(
                key="movie-5000", value=movie, ttl="24h"
            )

            print("hyper.cache.add_async result --> ", result)
            # OkResult - hyper.cache.add result -->  {'ok': True, 'status': 201}
            # NotOkResult - hyper.cache.add result -->  {'ok': False, 'status': 409, 'msg': 'Document Conflict'}

        Parameters
        ----------
        key : str
            - must begin with lowercase letter (`a-z`)
            - must be lowercase letters (`a-z`)
            - digits (`0-9`)
            - any of these characters `_ $ + -`

        value: Dict
            The value you wish to cache.
        ttl: str, optional
            instructs cache on how long the key/pair should remain in the cache
                - `s` seconds. eg: 20s = 20 seconds
                - `m` minutes. eg: 10m = 10 minutes
                - `h` hours. ex: 12h = 12 hours
                - `d` days. ex: 14d = 14 days
                - `w` weeks. ex: 1w = 1 week


        Returns
        -------
        Result.
        """
        return self._add_cache_sync(key, value, ttl)

    def get(self, key: str) -> HyperGetResult:
        """
        Returns a specific value cached for the specified key.

        Example:
            key = "movie-5000"
            result: HyperGetResult = hyper.cache.get(key)
            print("hyper.cache.get result --> ", result)
            # hyper.cache.get result -->  {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1987', 'status': 200}


        Parameters
        ----------
        key : str
            - must begin with lowercase letter (`a-z`)
            - must be lowercase letters (`a-z`)
            - digits (`0-9`)
            - any of these characters `_ $ + -`

        Returns
        -------
        HyperGetResult
        """
        return self._get_cache_sync(key)

    def set(self, key: str, value: Dict, ttl: Optional[str]) -> Result:
        """
        updates a document in the cache store.
        By updating the document you can modify the values of the document,
        as well as modify/extend the time to live or ttl.

        Example:

            movie: Dict = {
                "_id": "movie-5000",
                "type": "movie",
                "title": "Back to the Future 2",
                "year": "1988",
            }

            result = hyper.cache.set(
                key="movie-5000", value=movie, ttl="1w"
            )
            print("hyper.cache.set result --> ", result)
            # hyper.cache.set result -->  {'ok': True, 'status': 200}

        Parameters
        ----------
        key : str
            - must begin with lowercase letter (`a-z`)
            - must be lowercase letters (`a-z`)
            - digits (`0-9`)
            - any of these characters `_ $ + -`

        value: Dict
            The dictionary you wish to update within the cache.
        ttl: str, optional
            instructs cache on how long the key/pair should remain in the cache
                - `s` seconds. eg: 20s = 20 seconds
                - `m` minutes. eg: 10m = 10 minutes
                - `h` hours. ex: 12h = 12 hours
                - `d` days. ex: 14d = 14 days
                - `w` weeks. ex: 1w = 1 week

        Returns
        -------
        Result.
        """
        return self._set_cache_sync(key, value, ttl)

    def remove(self, key: str) -> Result:
        """
        Deletes the key/value pair from the cache store.

        Example:

            key = "movie-5000"
            result = hyper.cache.remove(key)
            print("hyper.cache.remove_async result --> ", result)
             # hyper.cache.remove_async result -->  {'ok': True, 'status': 200}


        Parameters
        ----------
        key : str
            - must begin with lowercase letter (`a-z`)
            - must be lowercase letters (`a-z`)
            - digits (`0-9`)
            - any of these characters `_ $ + -`

        Returns
        -------
        Result.
        """
        return self._remove_cache_sync(key)

    def query(self, pattern: str) -> HyperDocsResult:
        """
        query using a comparion pattern.
        When applied the pattern will be used to match all the keys
        in the cache and only return the ones that match the pattern.
        Using the * wildcard, you can define patterns like "movie*" that
        match all the key values that either start with the provided pattern,
        end with the pattern, or is in-between the pattern.
        Examples:
            - starts with "movie*"
            - ends with "*-1984"
            - in-bewteen "movie*1984"

        Example:
            result : HyperDocsResult = hyper.cache.query(pattern="movie-500*")
            print("hyper.cache.query result --> ", result)
            # hyper.cache.query result -->  {'docs': [{'key': 'movie-5001', 'value': {'_id': 'movie-5001', 'type': 'movie', 'title': 'Back to the Future 3', 'year': '1989'}}, {'key': 'movie-5000', 'value': {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1988'}}], 'ok': True, 'status': 200}

        Parameters
        ----------
        pattern : str


        Returns
        -------
        HyperDocsResult.
        """
        return self._post_cache_query_sync(pattern)


class HyperData:
    """
    A class to represent a hyper application's data service.
    A hyper data service is a document data store for storing documents.
    Query, add, update, and delete these documents using the hyper REST API.
    You can also create indexes to improve query performance.
    See: https://docs.hyper.io/data-api

    ...
    Methods
    -------
    add(doc):
        Adds a document to the data service.
    remove(id):
        Removes a document.
    get(id):
        Retrieves a document.
    update(id, doc):
        Updates a document.
    bulk(docs):
        Inserts documents.
    query(selector, options)
        Queries documents.
    list(options)
        Lists documents.
    index(name, fields)
        Creates an index to speed data retrieval.
    add_async(doc):
        Asynchronously adds a document to the data service.
    remove_async(id):
        Asynchronously removes a document from the data service.
    get_async(id):
        Asynchronously retrieves a doc from the data service.
    update_async(id, doc):
        Asynchronously updates a document to the data service.
    bulk_async(docs):
        Asynchronously inserts documents.
    query_async(selector, options)
        Asynchronously queries a data service.
    list_async(options)
        Asynchronously lists documents.
    index_async(name, fields)
        Asynchronously creates an index to speed data retrieval.
    """

    def __init__(
        self,
        # ASYNC
        add_data_doc_async_fn: Callable,
        get_data_doc_async_fn: Callable,
        list_data_docs_async_fn: Callable,
        update_data_doc_async_fn: Callable,
        remove_data_doc_async_fn: Callable,
        query_docs_async_fn: Callable,
        index_docs_async_fn: Callable,
        bulk_docs_async_fn: Callable,
        # SYNC
        add_data_doc_sync_fn: Callable,
        get_data_doc_sync_fn: Callable,
        list_data_docs_sync_fn: Callable,
        update_data_doc_sync_fn: Callable,
        remove_data_doc_sync_fn: Callable,
        query_docs_sync_fn: Callable,
        index_docs_sync_fn: Callable,
        bulk_docs_sync_fn: Callable,
    ):
        # ASYNC
        self._add_data_async_doc = add_data_doc_async_fn
        self._get_data_async_doc = get_data_doc_async_fn
        self._list_data_async_docs = list_data_docs_async_fn
        self._update_data_async_doc = update_data_doc_async_fn
        self._remove_data_async_doc = remove_data_doc_async_fn
        self._query_async_docs = query_docs_async_fn
        self._index_async_docs = index_docs_async_fn
        self._bulk_async_docs = bulk_docs_async_fn

        # SYNC
        self._add_data_sync_doc = add_data_doc_sync_fn
        self._get_data_sync_doc = get_data_doc_sync_fn
        self._list_data_sync_docs = list_data_docs_sync_fn
        self._update_data_sync_doc = update_data_doc_sync_fn
        self._remove_data_sync_doc = remove_data_doc_sync_fn
        self._query_sync_docs = query_docs_sync_fn
        self._index_sync_docs = index_docs_sync_fn
        self._bulk_sync_docs = bulk_docs_sync_fn

    # ASYNC
    def add_async(self, doc: Dict) -> IdResult:
        """
        Asynchronously adds a document to the hyper data service.

        Create your own unique _id in your document
        Use a field on each document to distinguish its type from other documents ie. type or docType.

        For more details, see REST API documentation:  https://docs.hyper.io/create-a-document#9n-post-appnamedataservicename

        Example:

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

        Parameters
        ----------
        doc : Dict
            Document that will be added to the data service.
            A document with one-to-many fields, an `_id` field is required.
            No other fields that start with `_` are allowed.
            Each field name must follow the following rules:
            - must begin with a lowercase letter (`a-z`), unless it is the `_id` field.
            - must be lowercase letters (`a-z`)
            - digits (`0-9`)
            - any of these characters `_ $ + -`

        Returns
        -------
        Promise of a IdResult (OkIdResult, NotOkResult).
        """
        return self._add_data_async_doc(doc)

    def get_async(self, id: str) -> HyperGetResult:
        """
        Asynchronously retrieves a document from the hyper data service.

        Example:

            id: str = "movie-5000"
            result: HyperGetResult = await hyper.data.get_async(id)
            print("hyper.data.get_async result --> ", result)
            # hyper.data.get_async result -->  {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1987', 'status': 200}


        Parameters
        ----------
        id : str
            unique document identifier

        Returns
        -------
        Promise of a HyperGetResult (Dict, NotOkResult).
        """
        return self._get_data_async_doc(id)

    def list_async(self, options: ListOptions) -> HyperDocsResult:
        """
        Asynchronously returns a list of documents from the hyper data service.

        Example:

            options: ListOptions = {
                "startkey": "book-000105",
                "endkey": "book-000106",
            }

            result: HyperDocsResult = await hyper.data.list_async(options)
            print("hyper.data.list_async result --> ", result)
            # hyper.data.list_async result -->  {'docs': [{'_id': 'book-000105', 'type': 'book', 'name': 'The Lorax 105', 'author': 'Dr. Suess', 'published': '1969'}, {'_id': 'book-000106', 'type': 'book', 'name': 'The Lorax 106', 'author': 'Dr. Suess', 'published': '1969'}], 'ok': True, 'status': 200}

        Parameters
        ----------
        options : ListOptions
            data list options

        Returns
        -------
        Promise of a HyperDocsResult (OkDocsResult, NotOkDocsResult).
        """
        return self._list_data_async_docs(options)

    def update_async(self, id: str, doc: Dict) -> IdResult:
        """
        Asynchronously updates an existing document in your data service.

        change or add any property on the document except the _id property, it must stay the same.
        If you need to change the _id, simply remove the existing document and create a new document with the new _id.

        The update command only supports full document updates, not partial updates.

        Example:

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

        Parameters
        ----------
        id : str
            unique document identifier
        doc: Dict
            document with one-to-many fields, an `_id` field is required.
            No other fields that start with `_` are allowed.
            Each field name must follow the following rules:
            - must begin with a lowercase letter (`a-z`), unless it is the `_id` field.
            - must be lowercase letters (`a-z`)
            - digits (`0-9`)
            - any of these characters `_ $ + -`

        Returns
        -------
        Promise of a IdResult (OkIdResult, NotOkResult).
        """
        return self._update_data_async_doc(id, doc)

    def remove_async(self, id: str) -> IdResult:
        """
        Asynchronously deletes a specified document in the datastore.

        Example:

            id: str = "movie-5001"
            result: IdResult = await hyper.data.remove_async(id)

            print("hyper.data.remove_async result --> ", result)
            # hyper.data.remove_async result -->  {'id': 'movie-5001', 'ok': True, 'status': 200}

        Parameters
        ----------
        id : str
            unique document identifier

        Returns
        -------
        Promise of a IdResult (OkIdResult, NotOkResult).
        """
        return self._remove_data_async_doc(id)

    def query_async(
        self, selector: Dict, options: QueryOptions
    ) -> HyperDocsResult:
        """
        Asynchronously query documents in your datastore

        Example: Return 3 books

            selector = {"type": "book"}

            options: QueryOptions = {
                "fields": ["_id", "name", "published"],
                "sort": None,
                "limit": 3,
                "useIndex": None,
            }

            result:HyperDocsResult = await hyper.data.query_async(selector, options)
            print("hyper.data.query_async result --> ", result)
            # hyper.data.query_async result -->  {'docs': [{'_id': 'book-000010', 'name': 'The Lorax', 'published': '1959'}, {'_id': 'book-000020', 'name': 'The Lumberjack named Lorax the tree slayer', 'published': '1969'}, {'_id': 'book-000100', 'name': 'The Lorax 100', 'published': '1969'}], 'ok': True, 'status': 200}


        Parameters
        ----------
        selector : Dict
            This is the filter clause of your query.
            Indicates the criteria must be met in order for the document to be returned in the set of documents.
            eg. `{ "type": "movie" }` indicates to return documents that have a `type` property with the value `movie`.

        options: QueryOptions
            data service query options

        Returns
        -------
        Promise of a HyperDocsResult (OkDocsResult, NotOkDocsResult)
        """
        return self._query_async_docs(selector, options)

    def index_async(self, name: str, fields: List[str]) -> Result:
        """
        Asynchronously creates an index within your datastore.
        Indexes are used to provide fast search when querying a data service.
        With this command, you can create a specific index that can be applied to your query command, for more efficient response times.

        Example: Creates index, run query using index

            name: str =  "idx_author_published"
            fields: List[str] = ["author", "published"]

            index_result: Result = await hyper.data.index_async(name, fields)

            print("index_async result --> ", index_result)
            # index_async result -->  {'ok': True, 'status': 201}

            selector = {"type": "book", "author": "James A. Michener"}

            options: QueryOptions = {
                "fields": ["author", "published"],
                "sort": [{"author": "DESC"}, {"published": "DESC"}],
                "useIndex": "idx_author_published"
            }

            result: HyperDocsResult = await hyper.data.query_async(selector, options)
            print("hyper.data.query_async result --> ", result)
            # hyper.data.query_async result -->  {'docs': [{'author': 'James A. Michener', 'published': '1985'}, {'author': 'James A. Michener', 'published': '1959'}, {'author': 'James A. Michener', 'published': '1947'}], 'ok': True, 'status': 200}


        Parameters
        ----------
        name : str
            The index name

        fields : List[str]
            A list of field names from your documents within the datastore.

        Returns
        -------
        Promise of a Result (OkResult, NotOkResult)
        """
        return self._index_async_docs(name, fields)

    def bulk_async(self, docs: List[Dict]) -> HyperDocsResult:
        """
        Asynchronously submit a list of documents for batch loading into the datastore.
        A bulk update can handle inserting, updating, and deleting documents.
        An `_id` is required for each document.
        Use the `_deleted: true` on a document to delete the document.
        eg: `{ "_id": "1005", "type": "movie", "title": "Caddyshack", _deleted: true }`
        When submitting bulk documents, the request payload size limit is 10MB.

        Example: Bulk insert many docs in a single call.

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
                }
            ]

            result: HyperDocsResult = await hyper.data.bulk_async(docs)
            print("hyper.data.bulk_async result --> ", result)
            # hyper.data.bulk_async result -->  {'results': [{'ok': True, 'id': 'movie-6000'}, {'ok': True, 'id': 'movie-6001'}, {'ok': True, 'id': 'movie-6002'}, {'ok': True, 'id': 'movie-6003'}, {'ok': True, 'id': 'movie-6004'}], 'ok': True, 'status': 201}


        Parameters
        ----------
        docs : List[Dict]
            The list of docs

        Returns
        -------
        Promise of a HyperDocsResult (OkDocsResult, NotOkDocsResult)
        """
        return self._bulk_async_docs(docs)

    # SYNC
    def add(self, doc: Dict) -> IdResult:
        """
        Adds a document to the hyper data service.

        Create your own unique _id in your document
        Use a field on each document to distinguish its type from other documents ie. type or docType.

        For more details, see REST API documentation:  https://docs.hyper.io/create-a-document#9n-post-appnamedataservicename

        Example:

            movie: Dict = {
                "_id": "movie-5000",
                "type": "movie",
                "title": "Back to the Future 2",
                "year": "1987",
            }

            result: IdResult = hyper.data.add(movie)
            print("hyper.data.add result --> ", result)
            # OKIdResult: hyper.data.add result -->  {'id': 'movie-4000', 'ok': True, 'status': 201}
            # NotOkResult: hyper.data.add result -->  {'ok': False, 'status': 409, 'msg': 'document conflict'}

        Parameters
        ----------
        doc : Dict
            Document that will be added to the data service.
            A document with one-to-many fields, an `_id` field is required.
            No other fields that start with `_` are allowed.
            Each field name must follow the following rules:
            - must begin with a lowercase letter (`a-z`), unless it is the `_id` field.
            - must be lowercase letters (`a-z`)
            - digits (`0-9`)
            - any of these characters `_ $ + -`

        Returns
        -------
        IdResult (OkIdResult, NotOkResult).
        """
        return self._add_data_sync_doc(doc)

    def get(self, id: str) -> HyperGetResult:
        """
        Retrieves a document from the hyper data service.

        Example:

            id: str = "movie-5000"
            result: HyperGetResult = hyper.data.get(id)
            print("hyper.data.get result --> ", result)
            # hyper.data.get result -->  {'_id': 'movie-5000', 'type': 'movie', 'title': 'Back to the Future 2', 'year': '1987', 'status': 200}


        Parameters
        ----------
        id : str
            unique document identifier

        Returns
        -------
        HyperGetResult (Dict, NotOkResult).
        """
        return self._get_data_sync_doc(id)

    def list(self, options: ListOptions) -> HyperDocsResult:
        """
        Returns a list of documents from the hyper data service.

        Example:

            options: ListOptions = {
                "startkey": "book-000105",
                "endkey": "book-000106",
            }

            result: HyperDocsResult = hyper.data.list(options)
            print("hyper.data.list result --> ", result)
            # hyper.data.list result -->  {'docs': [{'_id': 'book-000105', 'type': 'book', 'name': 'The Lorax 105', 'author': 'Dr. Suess', 'published': '1969'}, {'_id': 'book-000106', 'type': 'book', 'name': 'The Lorax 106', 'author': 'Dr. Suess', 'published': '1969'}], 'ok': True, 'status': 200}

        Parameters
        ----------
        options : ListOptions
            data list options

        Returns
        -------
        HyperDocsResult (OkDocsResult, NotOkDocsResult).
        """
        return self._list_data_sync_docs(options)

    def update(self, id: str, doc: Dict) -> IdResult:
        """
        Updates an existing document in your data service.

        change or add any property on the document except the _id property, it must stay the same.
        If you need to change the _id, simply remove the existing document and create a new document with the new _id.

        The update command only supports full document updates, not partial updates.

        Example:

            book: Dict = {
                "_id": "book-000100",
                "type": "book",
                "name": "The Lorax 100",
                "author": "Dr. Suess",
                "published": "1969",
            }

            result: IdResult = hyper.data.update("book-000100", book)
            print("hyper.data.update result --> ", result)
            # hyper.data.update result -->  {'ok': True, 'id': 'book-000100', 'status': 200}

        Parameters
        ----------
        id : str
            unique document identifier
        doc: Dict
            document with one-to-many fields, an `_id` field is required.
            No other fields that start with `_` are allowed.
            Each field name must follow the following rules:
            - must begin with a lowercase letter (`a-z`), unless it is the `_id` field.
            - must be lowercase letters (`a-z`)
            - digits (`0-9`)
            - any of these characters `_ $ + -`

        Returns
        -------
        IdResult (OkIdResult, NotOkResult).
        """
        return self._update_data_sync_doc(id, doc)

    def remove(self, id: str) -> IdResult:
        """
        Deletes a specified document in the datastore.

        Example:

            id: str = "movie-5001"
            result: IdResult = hyper.data.remove(id)

            print("hyper.data.remove result --> ", result)
            # hyper.data.remove result -->  {'id': 'movie-5001', 'ok': True, 'status': 200}

        Parameters
        ----------
        id : str
            unique document identifier

        Returns
        -------
        IdResult (OkIdResult, NotOkResult).
        """
        return self._remove_data_sync_doc(id)

    def query(self, selector: Dict, options: QueryOptions) -> HyperDocsResult:
        """
        Query documents in your datastore

        Example: Return 3 books

            selector = {"type": "book"}

            options: QueryOptions = {
                "fields": ["_id", "name", "published"],
                "sort": None,
                "limit": 3,
                "useIndex": None,
            }

            result:HyperDocsResult = hyper.data.query(selector, options)
            print("hyper.data.query result --> ", result)
            # hyper.data.query result -->  {'docs': [{'_id': 'book-000010', 'name': 'The Lorax', 'published': '1959'}, {'_id': 'book-000020', 'name': 'The Lumberjack named Lorax the tree slayer', 'published': '1969'}, {'_id': 'book-000100', 'name': 'The Lorax 100', 'published': '1969'}], 'ok': True, 'status': 200}


        Parameters
        ----------
        selector : Dict
            This is the filter clause of your query.
            Indicates the criteria must be met in order for the document to be returned in the set of documents.
            eg. `{ "type": "movie" }` indicates to return documents that have a `type` property with the value `movie`.

        options: QueryOptions
            data service query options

        Returns
        -------
        HyperDocsResult (OkDocsResult, NotOkDocsResult)
        """
        return self._query_sync_docs(selector, options)

    def index(self, name: str, fields: List[str]) -> Result:
        """
        Creates an index within your datastore.
        Indexes are used to provide fast search when querying a data service.
        With this command, you can create a specific index that can be applied to your query command, for more efficient response times.

        Example: Creates index, run query using index

            name: str =  "idx_author_published"
            fields: List[str] = ["author", "published"]

            index_result: Result = hyper.data.index(name, fields)

            print("index result --> ", index_result)
            # index result -->  {'ok': True, 'status': 201}

            selector = {"type": "book", "author": "James A. Michener"}

            options: QueryOptions = {
                "fields": ["author", "published"],
                "sort": [{"author": "DESC"}, {"published": "DESC"}],
                "useIndex": "idx_author_published"
            }

            result: HyperDocsResult =  hyper.data.query(selector, options)
            print("hyper.data.query result --> ", result)
            # hyper.data.query result -->  {'docs': [{'author': 'James A. Michener', 'published': '1985'}, {'author': 'James A. Michener', 'published': '1959'}, {'author': 'James A. Michener', 'published': '1947'}], 'ok': True, 'status': 200}


        Parameters
        ----------
        name : str
            The index name

        fields : List[str]
            A list of field names from your documents within the datastore.

        Returns
        -------
        Result (OkResult, NotOkResult)
        """
        return self._index_sync_docs(name, fields)

    def bulk(self, docs: List[Dict]) -> HyperDocsResult:
        """
        Submit a list of documents for batch loading into the datastore.
        A bulk update can handle inserting, updating, and deleting documents.
        An `_id` is required for each document.
        Use the `_deleted: true` on a document to delete the document.
        eg: `{ "_id": "1005", "type": "movie", "title": "Caddyshack", _deleted: true }`
        When submitting bulk documents, the request payload size limit is 10MB.

        Example: Bulk insert many docs in a single call.

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
                }
            ]

            result: HyperDocsResult = hyper.data.bulk(docs)
            print("hyper.data.bulk result --> ", result)
            # hyper.data.bulk result -->  {'results': [{'ok': True, 'id': 'movie-6000'}, {'ok': True, 'id': 'movie-6001'}, {'ok': True, 'id': 'movie-6002'}, {'ok': True, 'id': 'movie-6003'}, {'ok': True, 'id': 'movie-6004'}], 'ok': True, 'status': 201}


        Parameters
        ----------
        docs : List[Dict]
            The list of docs

        Returns
        -------
        HyperDocsResult (OkDocsResult, NotOkDocsResult)
        """
        return self._bulk_sync_docs(docs)


class HyperStorage:
    """
    A hyper storage service is a object storage bucket used to store unstructured data like images, videos, and files.
    Upload, download and remove files.
    See: https://docs.hyper.io/storage-api

    ...
    Methods
    -------
    upload(name, data):
        Adds unstructured data such as a text file, image, or video to a storage service bucket using FormData.
    download(name)
        Retrieves an object from a storage service bucket.
    remove(name: str)
        Deletes the object from the storage service bucket.
    upload_async(name, data):
        Asynchronously adds unstructured data such as a text file, image, or video to a storage service bucket using FormData.
    download_async(name)
        Asynchronously retrieves an object from a storage service bucket.
    remove_async(name: str)
        Asynchronously deletes the object from the storage service bucket.
    """

    def __init__(
        self,
        # ASYNC
        upload_async_fn: Callable,
        download_async_fn: Callable,
        remove_async_fn: Callable,
        # SYNC
        upload_sync_fn: Callable,
        download_sync_fn: Callable,
        remove_sync_fn: Callable,
    ):
        # ASYNC
        self._upload_async_fn = upload_async_fn
        self._download_async_fn = download_async_fn
        self._remove_async_fn = remove_async_fn
        # SYNC
        self._upload_sync_fn = upload_sync_fn
        self._download_sync_fn = download_sync_fn
        self._remove_sync_fn = remove_sync_fn

    # ASYNC
    def upload_async(self, name: str, data: io.BufferedReader) -> Result:
        """
        Asynchronously adds unstructured data such as a text file, image, or video to a storage service bucket using FormData.

        Example:
            # begin upload remix.png image file
            br_remix_png: io.BufferedReader = open(
                os.path.join(sys.path[0], "remix.png"), "rb"
            )
            br_remix_png_upload_result: Result = (
                await hyper.storage.upload_async(name="remix", data=br_remix_png)
            )

            br_remix_png.close()
            # end upload

            print("br_remix_png_upload_result ->", br_remix_png_upload_result)
            # br_remix_png_upload_result -> {'ok': True, 'status': 201}


        Parameters
        ----------
        name : str
            A name that uniquely identifies the object in the storage bucket.
            Typically the file name. Ex: "avatar.png"
        data: io.BufferedReader
            A buffered reader using a readable raw IO object such as a text file, image, or video.

        Returns
        -------
        Promise of a Result (OkResult, NotOkResult)
        """
        return self._upload_async_fn(name, data)

    def download_async(self, name: str) -> requests.Response:
        """
        Asynchronously retrieves an object from a storage service bucket.

        Example:
            br_remix_png_download_result: requests.Response = (
                await hyper.storage.download_async(name="remix")
            )

            # begin download of remix.png image file as remix_downloaded.png
            path = os.path.join(sys.path[0], "remix_downloaded.png")

            with open(path, "wb") as fd:
                for chunk in br_remix_png_download_result.iter_content(chunk_size=128):
                    fd.write(chunk)

            # end download

            print("br_remix_png_download_result ->", br_remix_png_download_result)
            # br_remix_png_download_result -> <Response [200]>

            print(br_remix_png_download_result.status_code)
            # 200

        Parameters
        ----------
        name : str
            A name that uniquely identifies the object in the storage bucket.
            Typically the file name. Ex: "avatar.png"

        Returns
        -------
        Promise of a Response See https://requests.readthedocs.io/en/latest/api/#requests.Response
        """
        #
        return self._download_async_fn(name)

    def remove_async(self, name: str) -> requests.Response:
        """
        Asynchronously deletes the object from the storage service bucket.

        Example:
            remove_result: Result = await hyper.storage.remove_async(name="remix-notfound")

        Parameters
        ----------
        name : str
            A name that uniquely identifies the object in the storage bucket.
            Typically the file name. Ex: "avatar.png"

        Returns
        -------
        Promise of a Result (OkResult, NotOkResult)
        """

        return self._remove_async_fn(name)

    # SYNC
    def upload(self, name: str, data: io.BufferedReader):
        """
         Adds unstructured data such as a text file, image, or video to a storage service bucket using FormData.

        Example:
            # begin upload remix.png image file
            br_remix_png: io.BufferedReader = open(
                os.path.join(sys.path[0], "remix.png"), "rb"
            )
            br_remix_png_upload_result: Result = hyper.storage.upload_async(name="remix", data=br_remix_png)

            br_remix_png.close()
            # end upload

            print("br_remix_png_upload_result ->", br_remix_png_upload_result)
            # br_remix_png_upload_result -> {'ok': True, 'status': 201}


        Parameters
        ----------
        name : str
            A name that uniquely identifies the object in the storage bucket.
            Typically the file name. Ex: "avatar.png"
        data: io.BufferedReader
            A buffered reader using a readable raw IO object such as a text file, image, or video.

        Returns
        -------
        Result (OkResult, NotOkResult)
        """
        return self._upload_sync_fn(name, data)

    def download(self, name: str):
        """
        Retrieves an object from a storage service bucket.

        Example:
            br_remix_png_download_result: requests.Response = hyper.storage.download_async(name="remix")


            # begin download of remix.png image file as remix_downloaded.png
            path = os.path.join(sys.path[0], "remix_downloaded.png")

            with open(path, "wb") as fd:
                for chunk in br_remix_png_download_result.iter_content(chunk_size=128):
                    fd.write(chunk)

            # end download

            print("br_remix_png_download_result ->", br_remix_png_download_result)
            # br_remix_png_download_result -> <Response [200]>

            print(br_remix_png_download_result.status_code)
            # 200

        Parameters
        ----------
        name : str
            A name that uniquely identifies the object in the storage bucket.
            Typically the file name. Ex: "avatar.png"

        Returns
        -------
        Response See https://requests.readthedocs.io/en/latest/api/#requests.Response
        """
        return self._download_sync_fn(name)

    def remove(self, name: str):
        """
        Deletes the object from the storage service bucket.

        Example:
            remove_result: Result = hyper.storage.remove_async(name="remix-notfound")

        Parameters
        ----------
        name : str
            A name that uniquely identifies the object in the storage bucket.
            Typically the file name. Ex: "avatar.png"

        Returns
        -------
        Result (OkResult, NotOkResult)
        """
        return self._remove_sync_fn(name)


class HyperQueue:
    def __init__(
        self,
        # ASYNC
        enqueue_async_fn: Callable,
        list_job_errors_async_fn: Callable,
        list_job_queued_async_fn: Callable,
        # SYNC
        enqueue_sync_fn: Callable,
        list_job_errors_sync_fn: Callable,
        list_job_queued_sync_fn: Callable,
    ):
        # ASYNC
        self._enqueue_async_fn = enqueue_async_fn
        self._list_errors_async_fn = list_job_errors_async_fn
        self._list_queued_async_fn = list_job_queued_async_fn
        # SYNC
        self._enqueue_sync_fn = enqueue_sync_fn
        self._list_errors_sync_fn = list_job_errors_sync_fn
        self._list_queued_sync_fn = list_job_queued_sync_fn

    # ASYNC
    def enqueue_async(self, job: Dict):
        return self._enqueue_async_fn(job)

    def errors_async(self):
        return self._list_errors_async_fn()

    def queued_async(self):
        return self._list_queued_async_fn()

    # SYNC
    def enqueue(self, job: Dict):
        return self._enqueue_sync_fn(job)

    def errors(self):
        return self._list_errors_sync_fn()

    def queued(self):
        return self._list_queued_sync_fn()


class HyperSearch:
    """
    A class to represent a hyper application's search service.
    A hyper search service is a search index.
    Index documents by adding them to your search service. Then query to perform a full text search.
    You'll need to create a hyper app and a search service.
    See https://docs.hyper.io/adding-a-search-service

    ...
    Methods
    -------
    add(key, doc):
        Indexes a document to the search service.
    remove(key):
        Removes a document from the search service.
    get(key):
        Retrieves an indexed doc by id.
    update(key, doc):
        Updates a document to the search service.
    load([...]):
        Inserts search documents using an array of documents.
    query(query, options)
        Queries a search service.  options argument is optional.
    add_async(key, doc):
        Asynchronously indexes a document to the search service.
    remove_async(key):
        Asynchronously removes a document from the search service.
    get_async(key):
        Asynchronously retrieves an indexed doc by id.
    update_async(key, doc):
        Asynchronously updates a document to the search service.
    load_async([...]):
        Asynchronously inserts search documents using an array of documents.
    query_async(query, options)
        Asynchronously queries a search service.  options argument is optional.
    """

    def __init__(
        self,
        # ASYNC
        add_search_doc_async_fn: Callable,
        remove_search_doc_async_fn: Callable,
        get_search_doc_async_fn: Callable,
        update_search_doc_async_fn: Callable,
        load_search_async_fn: Callable,
        query_search_async_fn: Callable,
        # SYNC
        add_search_doc_sync_fn: Callable,
        remove_search_doc_sync_fn: Callable,
        get_search_doc_sync_fn: Callable,
        update_search_doc_sync_fn: Callable,
        load_search_sync_fn: Callable,
        query_search_sync_fn: Callable,
    ):
        # ASYNC
        self._add_search_async_doc = add_search_doc_async_fn
        self._remove_search_async_doc = remove_search_doc_async_fn
        self._get_search_async_doc = get_search_doc_async_fn
        self._update_search_async_doc = update_search_doc_async_fn
        self._load_search_async = load_search_async_fn
        self._query_search_async = query_search_async_fn

        # SYNC
        self._add_search_sync_doc = add_search_doc_sync_fn
        self._remove_search_sync_doc = remove_search_doc_sync_fn
        self._get_search_sync_doc = get_search_doc_sync_fn
        self._update_search_sync_doc = update_search_doc_sync_fn
        self._load_search_sync = load_search_sync_fn
        self._query_search_sync = query_search_sync_fn

    # ASYNC
    def add_async(self, key: str, doc: Dict) -> IdResult:
        """
        Asynchronously adds a document to your search index. The document must have the fields specified by the mapping object when you created the index.
        Use the hyper cloud dashboard to create a search service/index.  https://dashboard.hyper.io/
        Adding a search service/index: https://docs.hyper.io/adding-a-search-service
        Example: https://github.com/hyper63/hyper-connect-py#add-document-into-search

        Parameters
        ----------
        key : str
            Unique identifier for the search index
        doc : Dict
            Document that will be added to the index

        Returns
        -------
        Promise of a Result (OkResult or NotOkResult).
        """
        return self._add_search_async_doc(key, doc)

    def remove_async(self, key: str) -> Result:
        """
        Asynchronously removes a document from the search service.
        Use the hyper cloud dashboard to create a search service/index.  https://dashboard.hyper.io/
        Adding a search service/index: https://docs.hyper.io/adding-a-search-service
        Example: https://github.com/hyper63/hyper-connect-py#remove-document-from-search

        Parameters
        ----------
        key : str
            Search document's key

        Returns
        -------
        Promise of a Result (OkResult or NotOkResult).
        """
        return self._remove_search_async_doc(key)

    def get_async(self, key: str) -> HyperGetResult:
        """
        Asynchronously gets a document from the search service.
        Use the hyper cloud dashboard to create a search service/index.  https://dashboard.hyper.io/
        Adding a search service/index: https://docs.hyper.io/adding-a-search-service
        Example: https://github.com/hyper63/hyper-connect-py#get-document-from-search

        Parameters
        ----------
        key : str
            Search document's key

        Returns
        -------
        Promise of a HyperGetResult.
        """
        return self._get_search_async_doc(key)

    def update_async(self, key: str, doc: Dict) -> Result:
        """
        Asynchronously updates a document to the search service.
        Use the hyper cloud dashboard to create a search service/index.  https://dashboard.hyper.io/
        Adding a search service/index: https://docs.hyper.io/adding-a-search-service
        Example: https://github.com/hyper63/hyper-connect-py#update-document-in-search

        Parameters
        ----------
        key : str
            Search document's key
        doc : Dict
            Search document

        Returns
        -------
        Promise of a Result (OkResult or NotOkResult).
        """
        return self._update_search_async_doc(key, doc)

    def load_async(self, docs: List[Dict]) -> HyperSearchLoadResult:
        """
         Asynchronously index multiple documents in one batch call to the server.
        Use the hyper cloud dashboard to create a search service/index.  https://dashboard.hyper.io/
         Adding a search service/index: https://docs.hyper.io/adding-a-search-service
         Example: https://github.com/hyper63/hyper-connect-py#bulk-load-into-search-1

         Parameters
         ----------
         docs : List[Dict]
             A list of documents to bulk load.  The _id property is required for each document.

         Returns
         -------
         Promise of a HyperSearchLoadResult.
        """
        return self._load_search_async(docs)

    def query_async(
        self, query: str, options: Optional[SearchQueryOptions]
    ) -> HyperSearchQueryResult:
        """
        Asynchronously query the search index by including a query the value of your search string. You can optionally include a options of type SearchQueryOptions  that contains a fields property containing a list of fields you would like to target the search against and a filter property which is an Dict of key/value pairs to filter the search results
        Use the hyper cloud dashboard to create a search service/index.  https://dashboard.hyper.io/
        Adding a search service/index: https://docs.hyper.io/adding-a-search-service
        Example: https://github.com/hyper63/hyper-connect-py#query-documents-in-search

        Parameters
        ----------
        query : str
            The text you would like to search for matches
        options : SearchQueryOptions, optional
            fields: A list of fields you would like to target the search against. Each string in the array should match a property in the Fields to store list in the indexed document.  See https://docs.hyper.io/adding-a-search-service.
            filter: key/value pairs that should reduce the results based on the result of the filter. Each key should match a property in the Fields to store list that you provided when you created the search index.

        Returns
        -------
        Promise of a HyperSearchQueryResult (HyperSearchQueryOKResult or NotOkResult).
        """
        return self._query_search_async(query, options)

    # SYNC
    def add(self, key: str, doc: Dict) -> Result:
        """
        Adds a document to your search index. The document must have the fields specified by the mapping object when you created the index.
        Use the hyper cloud dashboard to create a search service/index.  https://dashboard.hyper.io/
        Adding a search service/index: https://docs.hyper.io/adding-a-search-service
        Example: https://github.com/hyper63/hyper-connect-py#add-to-search

        Parameters
        ----------
        key : str
            Unique identifier for the search index
        doc : Dict
            Document that will be added to the index

        Returns
        -------
        Promise of a Result (OkResult or NotOkResult).
        """
        return self._add_search_sync_doc(key, doc)

    def remove(self, key: str) -> Result:
        """
        Removes a document from the search service.
        Use the hyper cloud dashboard to create a search service/index.  https://dashboard.hyper.io/
        Adding a search service/index: https://docs.hyper.io/adding-a-search-service
        Example: https://github.com/hyper63/hyper-connect-py#remove-from-search

        Parameters
        ----------
        key : str
            Search document's key

        Returns
        -------
        Promise of a Result (OkResult or NotOkResult).
        """
        return self._remove_search_sync_doc(key)

    def get(self, key: str) -> HyperGetResult:
        """
        Gets a document from the search service.
        Use the hyper cloud dashboard to create a search service/index.  https://dashboard.hyper.io/
        Adding a search service/index: https://docs.hyper.io/adding-a-search-service
        Example: https://github.com/hyper63/hyper-connect-py#get-from-search

        Parameters
        ----------
        key : str
            Search document's key

        Returns
        -------
        Promise of a HyperGetResult.
        """
        return self._get_search_sync_doc(key)

    def update(self, key: str, doc: Dict) -> Result:
        """
        updates a document to the search service.
        Use the hyper cloud dashboard to create a search service/index.  https://dashboard.hyper.io/
        Adding a search service/index: https://docs.hyper.io/adding-a-search-service
        Example: https://github.com/hyper63/hyper-connect-py#update-search

        Parameters
        ----------
        key : str
            Search document's key
        doc : Dict
            Search document

        Returns
        -------
        Promise of a Result (OkResult or NotOkResult).
        """
        return self._update_search_sync_doc(key, doc)

    def load(self, docs: List[Dict]) -> HyperSearchLoadResult:
        """
        Asynchronously index multiple documents in one batch call to the server.
        Use the hyper cloud dashboard to create a search service/index.  https://dashboard.hyper.io/
        Adding a search service/index: https://docs.hyper.io/adding-a-search-service
        Example: https://github.com/hyper63/hyper-connect-py#bulk-load-into-search

        Parameters
        ----------
        docs : List[Dict]
            A list of documents to bulk load.  The _id property is required for each document.

        Returns
        -------
        Promise of a HyperSearchLoadResult.
        """
        return self._load_search_sync(docs)

    def query(
        self, query: str, options: Optional[SearchQueryOptions]
    ) -> HyperSearchQueryResult:
        """
        Query the search index by including a query the value of your search string. You can optionally include a options of type SearchQueryOptions  that contains a fields property containing a list of fields you would like to target the search against and a filter property which is an Dict of key/value pairs to filter the search results
        Use the hyper cloud dashboard to create a search service/index.  https://dashboard.hyper.io/
        Adding a search service/index: https://docs.hyper.io/adding-a-search-service

        Parameters
        ----------
        query : str
            The text you would like to search for matches
        options : SearchQueryOptions, optional
            fields: A list of fields you would like to target the search against. Each string in the array should match a property in the Fields to store list in the indexed document.  See https://docs.hyper.io/adding-a-search-service.
            filter: key/value pairs that should reduce the results based on the result of the filter. Each key should match a property in the Fields to store list that you provided when you created the search index.

        Returns
        -------
        Promise of a HyperSearchQueryResult (HyperSearchQueryOKResult or NotOkResult).
        """
        return self._query_search_sync(query, options)


class HyperInfo:
    def __init__(self, services_async_fn: Callable, services_fn: Callable):
        self._services_async_fn = services_async_fn
        self._services_fn = services_fn

    def services_async(self):
        return self._services_async_fn()

    def services(
        self,
    ):
        return self._services_fn()


# Hyper Classes
class WriteHyperError(Exception):
    pass


class Hyper:
    """
    A class used to represent access to a hyper application's services, such as Data, Storage, Cache, Queue, and Search.
    Returned by hyper_connect's connect function.

    ...

    Attributes
    ----------
    data : HyperData
        The hyper app's Data service
    cache : HyperCache
        The hyper app's Cache service
    search : HyperSearch
        The hyper app's Search service
    storage : HyperStorage
        The hyper app's Storage service
    queue : HyperQueue
        The hyper app's Queue service
    info: HyperInfo
        The hyper app's Info service
    """

    def __init__(
        self,
        data: HyperData,
        cache: HyperCache,
        search: HyperSearch,
        storage: HyperStorage,
        queue: HyperQueue,
        info: HyperInfo,
    ):
        self._data = data
        self._cache = cache
        self._search = search
        self._storage = storage
        self._queue = queue
        self._info = info

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        raise WriteHyperError("data service property is read-only")

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, value):
        raise WriteHyperError("cache service property is read-only")

    @property
    def search(self):
        return self._search

    @search.setter
    def search(self, value):
        raise WriteHyperError("search service property is read-only")

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, value):
        raise WriteHyperError("storage service property is read-only")

    @property
    def queue(self):
        return self._queue

    @queue.setter
    def queue(self, value):
        raise WriteHyperError("queue service property is read-only")

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, value):
        raise WriteHyperError("info service property is read-only")
