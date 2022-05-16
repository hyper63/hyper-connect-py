from typing import Dict, List

from typeguard import typechecked

# from ._cache import addCacheDoc
from hyper_connect.services import (
    add_data,
    get_data,
    get_data_list,
    post_bulk,
    post_index,
    post_query,
    remove_data,
    update_data,
)
from hyper_connect.types import Hyper, HyperData, ListOptions, QueryOptions
from hyper_connect.utils import handle_response


@typechecked
def connect(CONNECTION_STRING: str, domain: str = "default") -> Hyper:
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

    hyperData: HyperData = HyperData(
        add_data_doc_fn=add_data_doc,
        get_data_doc_fn=get_data_doc,
        list_data_docs_fn=list_data_docs,
        update_data_doc_fn=update_data_doc,
        remove_data_doc_fn=remove_data_doc,
        query_docs_fn=query_docs,
        index_docs_fn=index_docs,
        bulk_docs_fn=bulk_docs,
    )

    hyper: Hyper = Hyper(data=hyperData)

    # hyper = {
    #     "data": {
    #         "add": lambda body: addData(body, CONNECTION_STRING, domain).then(
    #             handle_response
    #         )
    #     }
    # }
    return hyper
