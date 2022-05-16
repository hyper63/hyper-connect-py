from typing import Callable, Dict, List, Literal, Optional, TypedDict, Union

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
        self._addDataDoc = add_data_doc_fn
        self._getDataDoc = get_data_doc_fn
        self._listDataDocs = list_data_docs_fn
        self._updateDataDoc = update_data_doc_fn
        self._removeDataDoc = remove_data_doc_fn
        self._postDataQuery = query_docs_fn
        self._postDataIndex = index_docs_fn
        self._postBulk = bulk_docs_fn

    def add(self, doc: Dict):
        return self._addDataDoc(doc)

    def get(self, id: str):
        return self._getDataDoc(id)

    def list(self, options: ListOptions):
        return self._listDataDocs(options)

    def update(self, id: str, doc: Dict):
        return self._updateDataDoc(id, doc)

    def remove(self, id: str):
        return self._removeDataDoc(id)

    def query(self, selector: Dict, options: QueryOptions):
        return self._postDataQuery(selector, options)

    def index(self, name: str, fields: List[str]):
        return self._postDataIndex(name, fields)

    def bulk(self, docs: List[Dict]):
        return self._postBulk(docs)


# Hyper Classes
class WriteHyperError(Exception):
    pass


# def __init__(self, data, cache, search, storage, queue, info ):
class Hyper:
    def __init__(self, data: HyperData):
        self._data = data
        # self._cache = cache
        # self._search = search
        # self._storage = storage
        # self._queue = queue
        # self._info = info

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        raise WriteHyperError("data service property is read-only")

    # @property
    # def cache(self):
    #     return self._cache

    # @cache.setter
    # def cache(self, value):
    #     raise WriteHyperError("cache service property is read-only")

    # @property
    # def search(self):
    #     return self._search

    # @search.setter
    # def search(self, value):
    #     raise WriteHyperError("search service property is read-only")

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
