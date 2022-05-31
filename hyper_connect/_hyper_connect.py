import io
from typing import Any, Dict, List, Optional

from typeguard import typechecked

# from ._cache import addCacheDoc
from hyper_connect.services import (
    add_cache,
    add_data,
    add_search,
    download,
    get_cache,
    get_data,
    get_data_list,
    get_search,
    load_search,
    post_bulk,
    post_cache_query,
    post_index,
    post_query,
    post_query_search,
    queue_enqueue,
    queue_errors,
    queue_queued,
    remove_cache,
    remove_data,
    remove_search,
    remove_storage,
    services,
    set_cache,
    update_data,
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
from hyper_connect.utils import handle_response


@typechecked
def connect(CONNECTION_STRING: str, domain: str = "default") -> Hyper:

    # //////////////////////
    #      HyperData
    # //////////////////////

    def add_data_doc(doc: Dict):
        return add_data(doc, CONNECTION_STRING, domain).then(handle_response)

    def get_data_doc(id: str):
        return get_data(id, CONNECTION_STRING, domain).then(handle_response)

    def list_data_docs(options: ListOptions):
        return get_data_list(options, CONNECTION_STRING, domain).then(
            handle_response
        )

    def update_data_doc(id: str, doc: Dict):
        return update_data(id, doc, CONNECTION_STRING, domain).then(
            handle_response
        )

    def remove_data_doc(id: str):
        return remove_data(id, CONNECTION_STRING, domain).then(handle_response)

    def query_docs(selector: Dict, options: QueryOptions):
        return post_query(selector, options, CONNECTION_STRING, domain).then(
            handle_response
        )

    def index_docs(name: str, fields: List[str]):
        return post_index(name, fields, CONNECTION_STRING, domain).then(
            handle_response
        )

    def bulk_docs(docs: List[Dict]):
        return post_bulk(docs, CONNECTION_STRING, domain).then(handle_response)

    hyper_data: HyperData = HyperData(
        add_data_doc_async_fn=add_data_doc,
        get_data_doc_async_fn=get_data_doc,
        list_data_docs_async_fn=list_data_docs,
        update_data_doc_async_fn=update_data_doc,
        remove_data_doc_async_fn=remove_data_doc,
        query_docs_async_fn=query_docs,
        index_docs_async_fn=index_docs,
        bulk_docs_async_fn=bulk_docs,
    )

    # ////////////////////////////
    #     BEGIN HyperCache
    # ////////////////////////////

    # ////////////////////////////
    #          ASYNC
    # ////////////////////////////

    def add_cache_doc_async(key: str, value: Any, ttl: Optional[str]):
        return add_cache(key, value, ttl, CONNECTION_STRING, domain).then(
            handle_response
        )

    def get_cache_doc_async(key: str):
        return get_cache(key, CONNECTION_STRING, domain).then(handle_response)

    def set_cache_doc_async(key: str, value: Any, ttl: Optional[str]):
        return set_cache(key, value, ttl, CONNECTION_STRING, domain).then(
            handle_response
        )

    def remove_cache_doc_async(key: str):
        return remove_cache(key, CONNECTION_STRING, domain).then(
            handle_response
        )

    def post_cache_query_doc_async(pattern: str):
        return post_cache_query(pattern, CONNECTION_STRING, domain).then(
            handle_response
        )

    # ////////////////////////////
    #         END ASYNC
    # ////////////////////////////

    # ////////////////////////////
    #         BEGIN SYNC
    # ////////////////////////////
    async def add_cache_doc_sync(key: str, value: Any, ttl: Optional[str]):
        result = await add_cache(
            key, value, ttl, CONNECTION_STRING, domain
        ).then(handle_response)
        return result

    async def get_cache_doc_sync(key: str):
        result = await get_cache(key, CONNECTION_STRING, domain).then(
            handle_response
        )
        return result

    async def set_cache_doc_sync(key: str, value: Any, ttl: Optional[str]):
        result = await set_cache(
            key, value, ttl, CONNECTION_STRING, domain
        ).then(handle_response)
        return result

    async def remove_cache_doc_sync(key: str):
        result = await remove_cache(key, CONNECTION_STRING, domain).then(
            handle_response
        )
        return result

    async def post_cache_query_doc_sync(pattern: str):
        result = await post_cache_query(
            pattern, CONNECTION_STRING, domain
        ).then(handle_response)
        return result

    # ////////////////////////////
    #     END SYNC
    # ////////////////////////////

    hyper_cache: HyperCache = HyperCache(
        add_cache_async_fn=add_cache_doc_async,
        get_cache_async_fn=get_cache_doc_async,
        set_cache_async_fn=set_cache_doc_async,
        remove_cache_async_fn=remove_cache_doc_async,
        post_cache_query_async_fn=post_cache_query_doc_async,
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
