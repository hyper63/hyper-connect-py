from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    TypedDict,
    Union,
)

SortOptions = Literal["DESC", "ASC"]
ServiceType = Literal["data", "cache", "storage", "search", "queue", "info"]
Method = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
Action = Literal["_query", "_bulk", "_index"]
QueueStatus = Literal["ERROR", "READY"]


class ListOptions(TypedDict):
    limit: Optional[int]
    startkey: Optional[str]
    endkey: Optional[str]
    keys: Optional[List[str]]
    descending: Optional[bool]


class QueryOptions(TypedDict):
    fields: Optional[List[str]]
    sort: Optional[List[Dict[str, SortOptions]]]
    limit: Optional[int]
    useIndex: Optional[str]


class SearchQueryOptions(TypedDict):
    fields: Optional[List[str]]
    filter: Optional[Dict[str, str]]


class HyperRequest(TypedDict):
    service: ServiceType
    method: Method
    resource: Optional[str]
    body: Union[Dict, List[Dict], None]
    params: Union[ListOptions, QueryOptions, Dict[str, str], None]
    action: Optional[Action]


class RequestOptions(TypedDict):
    headers: Dict[str, str]
    method: Method
    body: Union[Dict, List[Dict], None]


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
    def __init__(
        self,
        add_cache_fn: Callable,
        get_cache_fn: Callable,
        set_cache_fn: Callable,
        remove_cache_fn: Callable,
        post_cache_query_fn: Callable,
    ):
        self._add_cache = add_cache_fn
        self._get_cache = get_cache_fn
        self._set_cache = set_cache_fn
        self._remove_cache = remove_cache_fn
        self._post_cache_query = post_cache_query_fn

    def add(self, key: str, value: Any, ttl: Optional[str]):
        return self._add_cache(key, value, ttl)

    def get(self, key: str):
        return self._get_cache(key)

    def set(self, key: str, value: Any, ttl: Optional[str]):
        return self._set_cache(key, value, ttl)

    def remove(self, key: str):
        return self._remove_cache(key)

    def query(self, pattern: str):
        return self._post_cache_query(pattern)


class HyperData:
    def __init__(
        self,
        add_data_doc_fn: Callable,
        get_data_doc_fn: Callable,
        list_data_docs_fn: Callable,
        update_data_doc_fn: Callable,
        remove_data_doc_fn: Callable,
        query_docs_fn: Callable,
        index_docs_fn: Callable,
        bulk_docs_fn: Callable,
    ):
        self._add_data_doc = add_data_doc_fn
        self._get_data_doc = get_data_doc_fn
        self._list_data_docs = list_data_docs_fn
        self._update_data_doc = update_data_doc_fn
        self._remove_data_doc = remove_data_doc_fn
        self._query_docs = query_docs_fn
        self._index_docs = index_docs_fn
        self._bulk_docs = bulk_docs_fn

    def add(self, doc: Dict):
        return self._add_data_doc(doc)

    def get(self, id: str):
        return self._get_data_doc(id)

    def list(self, options: ListOptions):
        return self._list_data_docs(options)

    def update(self, id: str, doc: Dict):
        return self._update_data_doc(id, doc)

    def remove(self, id: str):
        return self._remove_data_doc(id)

    def query(self, selector: Dict, options: QueryOptions):
        return self._query_docs(selector, options)

    def index(self, name: str, fields: List[str]):
        return self._index_docs(name, fields)

    def bulk(self, docs: List[Dict]):
        return self._bulk_docs(docs)


# ///////////////////////
# ////// BEGIN HERE
# ///////////////////////


class HyperSearch:
    def __init__(
        self,
        add_search_doc_fn: Callable,
        remove_search_doc_fn: Callable,
        get_search_doc_fn: Callable,
        update_search_doc_fn: Callable,
        load_search_fn: Callable,
        query_search_fn: Callable,
    ):
        self._add_search_doc = add_search_doc_fn
        self._remove_search_doc = remove_search_doc_fn
        self._get_search_doc = get_search_doc_fn
        self._update_search_doc = update_search_doc_fn
        self._load_search = load_search_fn
        self._query_search = query_search_fn

    def add(self, key: str, doc: Dict):
        return self._add_search_doc(key, doc)

    def remove(self, key: str):
        return self._remove_search_doc(key)

    def get(self, key: str):
        return self._get_search_doc(key)

    def update(self, key: str, doc: Dict):
        return self._update_search_doc(key, doc)

    def load(self, docs: List[Dict]):
        return self._load_search(docs)

    def query(self, query: str, options: Optional[SearchQueryOptions]):
        return self._query_search(query, options)


# Hyper Classes
class WriteHyperError(Exception):
    pass


# def __init__(self, data, cache, search, storage, queue, info ):
class Hyper:
    def __init__(
        self, data: HyperData, cache: HyperCache, search: HyperSearch
    ):
        self._data = data
        self._cache = cache
        self._search = search
        # self._storage = storage
        # self._queue = queue
        # self._info = info

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

    # @property
    # def storage(self):
    #     return self._storage

    # @storage.setter
    # def storage(self, value):
    #     raise WriteHyperError("storage service property is read-only")

    # @property
    # def queue(self):
    #     return self._queue

    # @queue.setter
    # def queue(self, value):
    #     raise WriteHyperError("queue service property is read-only")

    # @property
    # def info(self):
    #     return self._info

    # @info.setter
    # def info(self, value):
    #     raise WriteHyperError("info service property is read-only")
