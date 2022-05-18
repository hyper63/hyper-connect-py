import io
from typing import Any, Dict, List, Optional

from typeguard import typechecked

# from ._cache import addCacheDoc
from hyper_connect.services import (
    add_cache,
    add_data,
    add_search,
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
    remove_cache,
    remove_data,
    remove_search,
    set_cache,
    update_data,
    update_search,
    upload,
)
from hyper_connect.types import (
    Hyper,
    HyperCache,
    HyperData,
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
        return post_query(selector, options, CONNECTION_STRING, domain)

    def index_docs(name: str, fields: List[str]):
        return post_index(name, fields, CONNECTION_STRING, domain)

    def bulk_docs(docs: List[Dict]):
        return post_bulk(docs, CONNECTION_STRING, domain)

    hyper_data: HyperData = HyperData(
        add_data_doc_fn=add_data_doc,
        get_data_doc_fn=get_data_doc,
        list_data_docs_fn=list_data_docs,
        update_data_doc_fn=update_data_doc,
        remove_data_doc_fn=remove_data_doc,
        query_docs_fn=query_docs,
        index_docs_fn=index_docs,
        bulk_docs_fn=bulk_docs,
    )

    # //////////////////////
    #      HyperCache
    # //////////////////////

    def add_cache_doc(key: str, value: Any, ttl: Optional[str]):
        return add_cache(key, value, ttl, CONNECTION_STRING, domain).then(
            handle_response
        )

    def get_cache_doc(key: str):
        return get_cache(key, CONNECTION_STRING, domain)

    def set_cache_doc(key: str, value: Any, ttl: Optional[str]):
        return set_cache(key, value, ttl, CONNECTION_STRING, domain)

    def remove_cache_doc(key: str):
        return remove_cache(key, CONNECTION_STRING, domain)

    def post_cache_query_doc(pattern: str):
        return post_cache_query(pattern, CONNECTION_STRING, domain)

    hyper_cache: HyperCache = HyperCache(
        add_cache_fn=add_cache_doc,
        get_cache_fn=get_cache_doc,
        set_cache_fn=set_cache_doc,
        remove_cache_fn=remove_cache_doc,
        post_cache_query_fn=post_cache_query_doc,
    )

    # //////////////////////
    #      HyperSearch
    # //////////////////////

    def add_search_doc(key: str, doc: Dict):
        return add_search(key, doc, CONNECTION_STRING, domain).then(
            handle_response
        )

    def remove_search_doc(key: str):
        return remove_search(key, CONNECTION_STRING, domain)

    def get_search_doc(key: str):
        return get_search(key, CONNECTION_STRING, domain)

    def update_search_doc(key: str, doc: Dict):
        return update_search(key, doc, CONNECTION_STRING, domain)

    def load_search_docs(docs: List[Dict]):
        return load_search(docs, CONNECTION_STRING, domain)

    def post_query_search_docs(query: str, options: SearchQueryOptions):
        return post_query_search(query, options, CONNECTION_STRING, domain)

    hyper_search: HyperSearch = HyperSearch(
        add_search_doc_fn=add_search_doc,
        remove_search_doc_fn=remove_search_doc,
        get_search_doc_fn=get_search_doc,
        update_search_doc_fn=update_search_doc,
        load_search_fn=load_search_docs,
        query_search_fn=post_query_search_docs,
    )

    # //////////////////////
    #      HyperStorage
    # //////////////////////

    def upload_doc(name: str, data: io.BufferedReader):
        return upload(name, data, CONNECTION_STRING, domain).then(
            handle_response
        )

    hyper_storage: HyperStorage = HyperStorage(upload_fn=upload_doc)

    hyper: Hyper = Hyper(
        data=hyper_data,
        cache=hyper_cache,
        search=hyper_search,
        storage=hyper_storage,
    )

    return hyper
