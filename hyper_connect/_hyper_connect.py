from typing import Any, Dict, List

# from ._cache import addCacheDoc
from hyper_connect.services import (
    addData,
    getDataById,
    getDataList,
    postIndex,
    postQuery,
    removeDataById,
    updateData,
)
from hyper_connect.types import Hyper, HyperData, ListOptions, QueryOptions
from hyper_connect.utils import handle_response

# cache = {"add": addCacheDoc}

# >>> from hyper_connect import connect
# >>> hyper = connect('cloud://xmgta0num6j7n6un7aa6ouga26vqn784:cADh5FHDPWr5jE6qLDmCqQlMRkfUEWMsLPRaZ64EGFZImvUBx--gI1MkcrUqFPMR@cloud.hyper.io/express-quickstart','default')
# >>> result = await hyper.data.add(doc)


def connect(CONNECTION_STRING: str, domain: str = "default") -> Hyper:
    def printIdentity(prefix):
        def print_this(x):
            print(f"{prefix} -> {x}")

        return print_this

    def addDataDoc(doc: Dict):
        return addData(doc, CONNECTION_STRING, domain).then(handle_response)

    def getDataDoc(id: str):
        return getDataById(id, CONNECTION_STRING, domain).then(handle_response)

    def listDataDocs(options: ListOptions):
        return getDataList(options, CONNECTION_STRING, domain).then(handle_response)

    def updateDataDoc(id: str, doc: Dict):
        return updateData(id, doc, CONNECTION_STRING, domain).then(handle_response)

    def removeDataDoc(id: str):
        return removeDataById(id, CONNECTION_STRING, domain).then(handle_response)

    def queryDocs(selector: Dict, options: QueryOptions):
        return postQuery(selector, options, CONNECTION_STRING, domain)

    def indexDocs(name: str, fields: List[str]):
        return postIndex(name, fields, CONNECTION_STRING, domain)

    hyperData: HyperData = HyperData(
        addDataDocFn=addDataDoc,
        getDataDocFn=getDataDoc,
        listDataDocsFn=listDataDocs,
        updateDataDocFn=updateDataDoc,
        removeDataDocFn=removeDataDoc,
        postDataQueryFn=queryDocs,
        postDataIndexFn=indexDocs,
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
