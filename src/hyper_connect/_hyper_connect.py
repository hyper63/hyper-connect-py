import io
from typing import Any, Dict, List, Optional

from typeguard import typechecked

# from ._cache import addCacheDoc
from hyper_connect.services import (
    add_cache,
    add_cache_async,
    add_data,
    add_data_async,
    add_search,
    add_search_async,
    download,
    download_async,
    get_cache,
    get_cache_async,
    get_data,
    get_data_async,
    get_data_list,
    get_data_list_async,
    get_search,
    get_search_async,
    load_search,
    load_search_async,
    post_bulk,
    post_bulk_async,
    post_cache_query,
    post_cache_query_async,
    post_index,
    post_index_async,
    post_query,
    post_query_async,
    post_query_search,
    post_query_search_async,
    queue_enqueue,
    queue_enqueue_async,
    queue_errors,
    queue_errors_async,
    queue_queued,
    queue_queued_async,
    remove_cache,
    remove_cache_async,
    remove_data,
    remove_data_async,
    remove_search,
    remove_search_async,
    remove_storage,
    remove_storage_async,
    services,
    services_async,
    set_cache,
    set_cache_async,
    update_data,
    update_data_async,
    update_search,
    update_search_async,
    upload,
    upload_async,
)
from hyper_connect.types import (
    Hyper,
    HyperCache,
    HyperData,
    HyperInfo,
    HyperQueue,
    HyperSearch,
    HyperStorage,
    ListOptions,
    QueryOptions,
    SearchQueryOptions,
)
from hyper_connect.utils import handle_response, handle_response_sync

"""connects to a hyper cloud application

The API is split into five sections: data, cache, search, storage, and queue

Parameters
----------
CONNECTION_STRING : str
    A hyper application represents an application within hyper cloud.
    A hyper application contains app key pairs used to access its application services, such as Data, Storage, Cache, Queue, and Search.
    Each app key consists of a Key, Secret, and associated Connection String.
    A hyper cloud connection string consists of a key, secret, hyper cloud server, and hyper app name:
    cloud://<key>:<secret>@cloud.hyper.io/<hyper application name>
domain : str
    The service name. The default is "default".

Returns
-------
Hyper
    A Hyper object used to access application services, such as Data, Storage, Cache, Queue, and Search.

Examples
--------
>>> connection_string: str = str(config["HYPER"])
>>> hyper: Hyper = connect(connection_string)
"""


@typechecked
def connect(CONNECTION_STRING: str, domain: str = "default") -> Hyper:

    # /////////////////////////
    #      BEGIN HyperData
    # /////////////////////////

    # /////////////////////////
    #          ASYNC
    # /////////////////////////

    def add_data_doc_async(doc: Dict):
        return add_data_async(doc, CONNECTION_STRING, domain).then(
            handle_response
        )

    def get_data_doc_async(id: str):
        return get_data_async(id, CONNECTION_STRING, domain).then(
            handle_response
        )

    def list_data_docs_async(options: ListOptions):
        return get_data_list_async(options, CONNECTION_STRING, domain).then(
            handle_response
        )

    def update_data_doc_async(id: str, doc: Dict):
        return update_data_async(id, doc, CONNECTION_STRING, domain).then(
            handle_response
        )

    def remove_data_doc_async(id: str):
        return remove_data_async(id, CONNECTION_STRING, domain).then(
            handle_response
        )

    def query_docs_async(selector: Dict, options: QueryOptions):
        return post_query_async(
            selector, options, CONNECTION_STRING, domain
        ).then(handle_response)

    def index_docs_async(name: str, fields: List[str]):
        return post_index_async(name, fields, CONNECTION_STRING, domain).then(
            handle_response
        )

    def bulk_docs_async(docs: List[Dict]):
        return post_bulk_async(docs, CONNECTION_STRING, domain).then(
            handle_response
        )

    # ////////////////////////////
    #           SYNC
    # ////////////////////////////

    def add_data_doc_sync(doc: Dict):
        response = add_data(doc, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    def get_data_doc_sync(id: str):
        response = get_data(id, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    def list_data_docs_sync(options: ListOptions):
        response = get_data_list(options, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    def update_data_doc_sync(id: str, doc: Dict):
        response = update_data(id, doc, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    def remove_data_doc_sync(id: str):
        response = remove_data(id, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    def query_docs_sync(selector: Dict, options: QueryOptions):
        response = post_query(selector, options, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    def index_docs_sync(name: str, fields: List[str]):
        response = post_index(name, fields, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    def bulk_docs_sync(docs: List[Dict]):
        response = post_bulk(docs, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    hyper_data: HyperData = HyperData(
        # Async
        add_data_doc_async_fn=add_data_doc_async,
        get_data_doc_async_fn=get_data_doc_async,
        list_data_docs_async_fn=list_data_docs_async,
        update_data_doc_async_fn=update_data_doc_async,
        remove_data_doc_async_fn=remove_data_doc_async,
        query_docs_async_fn=query_docs_async,
        index_docs_async_fn=index_docs_async,
        bulk_docs_async_fn=bulk_docs_async,
        # Sync
        add_data_doc_sync_fn=add_data_doc_sync,
        get_data_doc_sync_fn=get_data_doc_sync,
        list_data_docs_sync_fn=list_data_docs_sync,
        update_data_doc_sync_fn=update_data_doc_sync,
        remove_data_doc_sync_fn=remove_data_doc_sync,
        query_docs_sync_fn=query_docs_sync,
        index_docs_sync_fn=index_docs_sync,
        bulk_docs_sync_fn=bulk_docs_sync,
    )
    # /////////////////////////
    #      END HyperData
    # /////////////////////////

    # ////////////////////////////
    #     BEGIN HyperCache
    # ////////////////////////////

    # ////////////////////////////
    #          ASYNC
    # ////////////////////////////

    def add_cache_doc_async(key: str, value: Any, ttl: Optional[str]):
        return add_cache_async(
            key, value, ttl, CONNECTION_STRING, domain
        ).then(handle_response)

    def get_cache_doc_async(key: str):
        return get_cache_async(key, CONNECTION_STRING, domain).then(
            handle_response
        )

    def set_cache_doc_async(key: str, value: Any, ttl: Optional[str]):
        return set_cache_async(
            key, value, ttl, CONNECTION_STRING, domain
        ).then(handle_response)

    def remove_cache_doc_async(key: str):
        return remove_cache_async(key, CONNECTION_STRING, domain).then(
            handle_response
        )

    def post_cache_query_doc_async(pattern: str):
        return post_cache_query_async(pattern, CONNECTION_STRING, domain).then(
            handle_response
        )

    # ////////////////////////////
    #            SYNC
    # ////////////////////////////
    def add_cache_doc_sync(key: str, value: Any, ttl: Optional[str]):
        response = add_cache(key, value, ttl, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    def get_cache_doc_sync(key: str):
        response = get_cache(key, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    def set_cache_doc_sync(key: str, value: Any, ttl: Optional[str]):
        response = set_cache(key, value, ttl, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    def remove_cache_doc_sync(key: str):
        response = remove_cache(key, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    def post_cache_query_doc_sync(pattern: str):
        response = post_cache_query(pattern, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    hyper_cache: HyperCache = HyperCache(
        # Async
        add_cache_async_fn=add_cache_doc_async,
        get_cache_async_fn=get_cache_doc_async,
        set_cache_async_fn=set_cache_doc_async,
        remove_cache_async_fn=remove_cache_doc_async,
        post_cache_query_async_fn=post_cache_query_doc_async,
        # Sync
        add_cache_sync_fn=add_cache_doc_sync,
        get_cache_sync_fn=get_cache_doc_sync,
        set_cache_sync_fn=set_cache_doc_sync,
        remove_cache_sync_fn=remove_cache_doc_sync,
        post_cache_query_sync_fn=post_cache_query_doc_sync,
    )
    # ////////////////////////////
    #     END HyperCache
    # ////////////////////////////

    # ////////////////////////////
    #      BEGIN HyperSearch
    # ////////////////////////////

    # ////////////////////////////
    #          ASYNC
    # ////////////////////////////

    def add_search_doc_async(key: str, doc: Dict):
        return add_search_async(key, doc, CONNECTION_STRING, domain).then(
            handle_response
        )

    def remove_search_doc_async(key: str):
        return remove_search_async(key, CONNECTION_STRING, domain).then(
            handle_response
        )

    def get_search_doc_async(key: str):
        return get_search_async(key, CONNECTION_STRING, domain).then(
            handle_response
        )

    def update_search_doc_async(key: str, doc: Dict):
        return update_search_async(key, doc, CONNECTION_STRING, domain).then(
            handle_response
        )

    def load_search_docs_async(docs: List[Dict]):
        return load_search_async(docs, CONNECTION_STRING, domain).then(
            handle_response
        )

    def post_query_search_docs_async(query: str, options: SearchQueryOptions):
        return post_query_search_async(
            query, options, CONNECTION_STRING, domain
        ).then(handle_response)

    # ////////////////////////////
    #          SYNC
    # ////////////////////////////
    def add_search_doc_sync(key: str, doc: Dict):
        response = add_search(key, doc, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    def remove_search_doc_sync(key: str):
        response = remove_search(key, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    def get_search_doc_sync(key: str):
        response = get_search(key, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    def update_search_doc_sync(key: str, doc: Dict):
        response = update_search(key, doc, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    def load_search_docs_sync(docs: List[Dict]):
        response = load_search(docs, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    def post_query_search_docs_sync(query: str, options: SearchQueryOptions):
        response = post_query_search(query, options, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    hyper_search: HyperSearch = HyperSearch(
        # Async
        add_search_doc_async_fn=add_search_doc_async,
        remove_search_doc_async_fn=remove_search_doc_async,
        get_search_doc_async_fn=get_search_doc_async,
        update_search_doc_async_fn=update_search_doc_async,
        load_search_async_fn=load_search_docs_async,
        query_search_async_fn=post_query_search_docs_async,
        # Sync
        add_search_doc_sync_fn=add_search_doc_sync,
        remove_search_doc_sync_fn=remove_search_doc_sync,
        get_search_doc_sync_fn=get_search_doc_sync,
        update_search_doc_sync_fn=update_search_doc_sync,
        load_search_sync_fn=load_search_docs_sync,
        query_search_sync_fn=post_query_search_docs_sync,
    )

    # ////////////////////////////
    #      END HyperSearch
    # ////////////////////////////

    # ///////////////////////////
    #      BEGIN HyperStorage
    # ///////////////////////////

    # ////////////////////////////
    #          ASYNC
    # ////////////////////////////

    def upload_doc_async(name: str, data: io.BufferedReader):
        return upload_async(name, data, CONNECTION_STRING, domain).then(
            handle_response
        )

    def download_doc_async(name: str):
        return download_async(name, CONNECTION_STRING, domain)

    def remove_storage_doc_async(name: str):
        return remove_storage_async(name, CONNECTION_STRING, domain).then(
            handle_response
        )

    # ////////////////////////////
    #            SYNC
    # ////////////////////////////

    def upload_doc_sync(name: str, data: io.BufferedReader):
        response = upload(name, data, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    def download_doc_sync(name: str):
        return download(name, CONNECTION_STRING, domain)

    def remove_storage_doc_sync(name: str):
        response = remove_storage(name, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    hyper_storage: HyperStorage = HyperStorage(
        # Async
        upload_async_fn=upload_doc_async,
        download_async_fn=download_doc_async,
        remove_async_fn=remove_storage_doc_async,
        # Sync
        upload_sync_fn=upload_doc_sync,
        download_sync_fn=download_doc_sync,
        remove_sync_fn=remove_storage_doc_sync,
    )
    # ///////////////////////////
    #      END HyperStorage
    # ///////////////////////////

    # /////////////////////////
    #      BEGIN HyperQueue
    # /////////////////////////

    # ////////////////////////////
    #          ASYNC
    # ////////////////////////////

    def enqueue_job_async(job: Dict):
        return queue_enqueue_async(job, CONNECTION_STRING, domain).then(
            handle_response
        )

    def list_job_errors_async():
        return queue_errors_async(CONNECTION_STRING, domain).then(
            handle_response
        )

    def list_job_queued_async():
        return queue_queued_async(CONNECTION_STRING, domain).then(
            handle_response
        )

    # ////////////////////////////
    #            SYNC
    # ////////////////////////////

    def enqueue_job_sync(job: Dict):
        response = queue_enqueue(job, CONNECTION_STRING, domain)
        return handle_response_sync(response)

    def list_job_errors_sync():
        response = queue_errors(CONNECTION_STRING, domain)
        return handle_response_sync(response)

    def list_job_queued_sync():
        response = queue_queued(CONNECTION_STRING, domain)
        return handle_response_sync(response)

    hyper_queue: HyperQueue = HyperQueue(
        # Async
        enqueue_async_fn=enqueue_job_async,
        list_job_errors_async_fn=list_job_errors_async,
        list_job_queued_async_fn=list_job_queued_async,
        # Sync
        enqueue_sync_fn=enqueue_job_sync,
        list_job_errors_sync_fn=list_job_errors_sync,
        list_job_queued_sync_fn=list_job_queued_sync,
    )
    # /////////////////////////
    #      END HyperQueue
    # /////////////////////////

    # /////////////////////////
    #      BEGIN HyperInfo
    # /////////////////////////

    def get_services_async():
        return services_async(CONNECTION_STRING, domain).then(handle_response)

    def get_services_sync():
        response = services(CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    hyper_info: HyperInfo = HyperInfo(
        services_async_fn=get_services_async, services_fn=get_services_sync
    )

    # /////////////////////////
    #      END HyperInfo
    # /////////////////////////

    hyper: Hyper = Hyper(
        data=hyper_data,
        cache=hyper_cache,
        search=hyper_search,
        storage=hyper_storage,
        queue=hyper_queue,
        info=hyper_info,
    )

    return hyper
