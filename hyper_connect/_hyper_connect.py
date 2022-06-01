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
    download,
    get_cache,
    get_cache_async,
    get_data,
    get_data_async,
    get_data_list,
    get_data_list_async,
    get_search,
    load_search,
    post_bulk,
    post_bulk_async,
    post_cache_query,
    post_cache_query_async,
    post_index,
    post_index_async,
    post_query,
    post_query_async,
    post_query_search,
    queue_enqueue,
    queue_errors,
    queue_queued,
    remove_cache,
    remove_cache_async,
    remove_data,
    remove_data_async,
    remove_search,
    remove_storage,
    services,
    set_cache,
    set_cache_async,
    update_data,
    update_data_async,
    update_search,
    upload,
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
    #         END ASYNC
    # ////////////////////////////

    # ////////////////////////////
    #         BEGIN SYNC
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

    # ////////////////////////////
    #     END SYNC
    # ////////////////////////////

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
    #         END ASYNC
    # ////////////////////////////

    # ////////////////////////////
    #         BEGIN SYNC
    # ////////////////////////////
    def add_cache_doc_sync(key: str, value: Any, ttl: Optional[str]):
        response = add_cache(key, value, ttl, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    def get_cache_doc_sync(key: str):
        response = get_cache(key, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    def set_cache_doc_sync(key: str, value: Any, ttl: Optional[str]):
        response = set_cache(key, value, ttl, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    def remove_cache_doc_sync(key: str):
        response = remove_cache(key, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    def post_cache_query_doc_sync(pattern: str):
        response = post_cache_query(pattern, CONNECTION_STRING, domain)
        result = handle_response_sync(response)
        return result

    # ////////////////////////////
    #     END SYNC
    # ////////////////////////////

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

    def add_search_doc(key: str, doc: Dict):
        return add_search(key, doc, CONNECTION_STRING, domain).then(
            handle_response
        )

    def remove_search_doc(key: str):
        return remove_search(key, CONNECTION_STRING, domain).then(
            handle_response
        )

    def get_search_doc(key: str):
        return get_search(key, CONNECTION_STRING, domain).then(handle_response)

    def update_search_doc(key: str, doc: Dict):
        return update_search(key, doc, CONNECTION_STRING, domain).then(
            handle_response
        )

    def load_search_docs(docs: List[Dict]):
        return load_search(docs, CONNECTION_STRING, domain).then(
            handle_response
        )

    def post_query_search_docs(query: str, options: SearchQueryOptions):
        return post_query_search(
            query, options, CONNECTION_STRING, domain
        ).then(handle_response)

    hyper_search: HyperSearch = HyperSearch(
        add_search_doc_async_fn=add_search_doc,
        remove_search_doc_async_fn=remove_search_doc,
        get_search_doc_async_fn=get_search_doc,
        update_search_doc_async_fn=update_search_doc,
        load_search_async_fn=load_search_docs,
        query_search_async_fn=post_query_search_docs,
    )

    # ////////////////////////////
    #      END HyperSearch
    # ////////////////////////////

    # ///////////////////////////
    #      BEGIN HyperStorage
    # ///////////////////////////

    def upload_doc(name: str, data: io.BufferedReader):
        return upload(name, data, CONNECTION_STRING, domain).then(
            handle_response
        )

    def download_doc(name: str):
        return download(name, CONNECTION_STRING, domain)

    def remove_storage_doc(name: str):
        return remove_storage(name, CONNECTION_STRING, domain).then(
            handle_response
        )

    hyper_storage: HyperStorage = HyperStorage(
        upload_async_fn=upload_doc,
        download_async_fn=download_doc,
        remove_async_fn=remove_storage_doc,
    )
    # ///////////////////////////
    #      END HyperStorage
    # ///////////////////////////

    # /////////////////////////
    #      BEGIN HyperQueue
    # /////////////////////////
    def enqueue_job(job: Dict):
        return queue_enqueue(job, CONNECTION_STRING, domain).then(
            handle_response
        )

    def list_job_errors():
        return queue_errors(CONNECTION_STRING, domain).then(handle_response)

    def list_job_queued():
        return queue_queued(CONNECTION_STRING, domain).then(handle_response)

    hyper_queue: HyperQueue = HyperQueue(
        enqueue_async_fn=enqueue_job,
        list_job_errors_async_fn=list_job_errors,
        list_job_queued_async_fn=list_job_queued,
    )
    # /////////////////////////
    #      END HyperQueue
    # /////////////////////////

    # /////////////////////////
    #      BEGIN HyperInfo
    # /////////////////////////

    def get_services():
        return services(CONNECTION_STRING, domain).then(handle_response)

    hyper_info: HyperInfo = HyperInfo(services_fn=get_services)

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
