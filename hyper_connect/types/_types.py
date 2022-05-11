from typing import Any, Callable, Dict, List, Literal, Optional, TypedDict, Union

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
    body: Optional[str]
    params: Union[ListOptions, QueryOptions, None]
    action: Optional[Action]


class RequestOptions(TypedDict):
    headers: Dict[str, str]
    method: Method
    body: Optional[Any]


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


# HyperData Class
class WriteHyperDataError(Exception):
    pass


class HyperData:
    def __init__(
        self, addDataDocFn: Callable, getDataDocFn: Callable, listDataDocsFn: Callable
    ):
        self._addDataDoc = addDataDocFn
        self._getDataDoc = getDataDocFn
        self._listDataDocs = listDataDocsFn

    def add(self, doc):
        return self._addDataDoc(doc)

    def get(self, id: str):
        return self._getDataDoc(id)

    def list(self, options: ListOptions):
        return self._listDataDocs(options)

    # @add.setter
    # def add(self, value):
    #     raise WriteHyperDataError("HyperData add property is read-only")

    # @property
    # def get(self):
    #     return self._get

    # @get.setter
    # def get(self, value):
    #     raise WriteHyperDataError("HyperData get property is read-only")


# Hyper Class
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
