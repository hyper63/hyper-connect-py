import io
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
    def add_async(self, key: str, value: Any, ttl: Optional[str]):
        return self._add_cache_async(key, value, ttl)

    def get_async(self, key: str):
        return self._get_cache_async(key)

    def set_async(self, key: str, value: Any, ttl: Optional[str]):
        return self._set_cache_async(key, value, ttl)

    def remove_async(self, key: str):
        return self._remove_cache_async(key)

    def query_async(self, pattern: str):
        return self._post_cache_query_async(pattern)

    # SYNC
    def add(self, key: str, value: Any, ttl: Optional[str]):
        return self._add_cache_sync(key, value, ttl)

    def get(self, key: str):
        return self._get_cache_sync(key)

    def set(self, key: str, value: Any, ttl: Optional[str]):
        return self._set_cache_sync(key, value, ttl)

    def remove(self, key: str):
        return self._remove_cache_sync(key)

    def query(self, pattern: str):
        return self._post_cache_query_sync(pattern)


class HyperData:
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
    def add_async(self, doc: Dict):
        return self._add_data_async_doc(doc)

    def get_async(self, id: str):
        return self._get_data_async_doc(id)

    def list_async(self, options: ListOptions):
        return self._list_data_async_docs(options)

    def update_async(self, id: str, doc: Dict):
        return self._update_data_async_doc(id, doc)

    def remove_async(self, id: str):
        return self._remove_data_async_doc(id)

    def query_async(self, selector: Dict, options: QueryOptions):
        return self._query_async_docs(selector, options)

    def index_async(self, name: str, fields: List[str]):
        return self._index_async_docs(name, fields)

    def bulk_async(self, docs: List[Dict]):
        return self._bulk_async_docs(docs)

    # SYNC
    def add(self, doc: Dict):
        return self._add_data_sync_doc(doc)

    def get(self, id: str):
        return self._get_data_sync_doc(id)

    def list(self, options: ListOptions):
        return self._list_data_sync_docs(options)

    def update(self, id: str, doc: Dict):
        return self._update_data_sync_doc(id, doc)

    def remove(self, id: str):
        return self._remove_data_sync_doc(id)

    def query(self, selector: Dict, options: QueryOptions):
        return self._query_sync_docs(selector, options)

    def index(self, name: str, fields: List[str]):
        return self._index_sync_docs(name, fields)

    def bulk(self, docs: List[Dict]):
        return self._bulk_sync_docs(docs)


class HyperStorage:
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
    def upload_async(self, name: str, data: io.BufferedReader):
        return self._upload_async_fn(name, data)

    def download_async(self, name: str):
        return self._download_async_fn(name)

    def remove_async(self, name: str):
        return self._remove_async_fn(name)

    # SYNC
    def upload(self, name: str, data: io.BufferedReader):
        return self._upload_sync_fn(name, data)

    def download(self, name: str):
        return self._download_sync_fn(name)

    def remove(self, name: str):
        return self._remove_sync_fn(name)


class HyperQueue:
    def __init__(
        self,
        enqueue_async_fn: Callable,
        list_job_errors_async_fn: Callable,
        list_job_queued_async_fn: Callable,
    ):
        self._enqueue_async_fn = enqueue_async_fn
        self._list_errors_async_fn = list_job_errors_async_fn
        self._list_queued_async_fn = list_job_queued_async_fn

    def enqueue_async(self, job: Dict):
        return self._enqueue_async_fn(job)

    def errors_async(self):
        return self._list_errors_async_fn()

    def queued_async(self):
        return self._list_queued_async_fn()


class HyperSearch:
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
    def add_async(self, key: str, doc: Dict):
        return self._add_search_async_doc(key, doc)

    def remove_async(self, key: str):
        return self._remove_search_async_doc(key)

    def get_async(self, key: str):
        return self._get_search_async_doc(key)

    def update_async(self, key: str, doc: Dict):
        return self._update_search_async_doc(key, doc)

    def load_async(self, docs: List[Dict]):
        return self._load_search_async(docs)

    def query_async(self, query: str, options: Optional[SearchQueryOptions]):
        return self._query_search_async(query, options)

    # SYNC
    def add(self, key: str, doc: Dict):
        return self._add_search_sync_doc(key, doc)

    def remove(self, key: str):
        return self._remove_search_sync_doc(key)

    def get(self, key: str):
        return self._get_search_sync_doc(key)

    def update(self, key: str, doc: Dict):
        return self._update_search_sync_doc(key, doc)

    def load(self, docs: List[Dict]):
        return self._load_search_sync(docs)

    def query(self, query: str, options: Optional[SearchQueryOptions]):
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


# def __init__(self, data, cache, search, storage, queue, info ):
class Hyper:
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
