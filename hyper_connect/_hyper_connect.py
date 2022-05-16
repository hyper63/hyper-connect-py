from typing import Dict, List

from typeguard import typechecked

# from ._cache import addCacheDoc
from hyper_connect.services import (
    addData,
    getDataById,
    getDataList,
    postBulk,
    postIndex,
    postQuery,
    removeDataById,
    updateData,
)
from hyper_connect.types import Hyper, HyperData, ListOptions, QueryOptions
from hyper_connect.utils import handle_response


@typechecked
def connect(CONNECTION_STRING: str, domain: str = "default") -> Hyper:
    def addDataDoc(doc: Dict):
        return addData(doc, CONNECTION_STRING, domain).then(handle_response)

    def getDataDoc(id: str):
        return getDataById(id, CONNECTION_STRING, domain).then(handle_response)

    def listDataDocs(options: ListOptions):
        return getDataList(options, CONNECTION_STRING, domain).then(
            handle_response
        )

    def updateDataDoc(id: str, doc: Dict):
        return updateData(id, doc, CONNECTION_STRING, domain).then(
            handle_response
        )

    def removeDataDoc(id: str):
        return removeDataById(id, CONNECTION_STRING, domain).then(
            handle_response
        )

    def queryDocs(selector: Dict, options: QueryOptions):
        return postQuery(selector, options, CONNECTION_STRING, domain)

    def indexDocs(name: str, fields: List[str]):
        return postIndex(name, fields, CONNECTION_STRING, domain)

    def bulkDocs(docs: List[Dict]):
        return postBulk(docs, CONNECTION_STRING, domain)

    hyperData: HyperData = HyperData(
        addDataDocFn=addDataDoc,
        getDataDocFn=getDataDoc,
        listDataDocsFn=listDataDocs,
        updateDataDocFn=updateDataDoc,
        removeDataDocFn=removeDataDoc,
        postDataQueryFn=queryDocs,
        postDataIndexFn=indexDocs,
        postBulkFn=bulkDocs,
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
