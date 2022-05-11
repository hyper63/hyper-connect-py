<h1 align="center">⚡️ hyper_connect ⚡️</h1>
<p align="center">
hyper_connect is a python package for <a href="https://docs.hyper.io">hyper</a>
</p>
<p align="center">

## Install

The following command will install the latest version of a module and its dependencies from the Python Packaging Index:

```
pip install hyper_connect
```

## Getting Started

`hyper_connect` wraps your hyper app's REST API, generating a short-lived JWT using a [connection string](https://docs.hyper.io/app-keys) from one of your hyper app's app keys.

A call to the `connect` function returns a `Hyper` object.

```
from hyper_connect import connect
from hyper_connect.types import Hyper

hyper: Hyper = connect(
    "<your hyper app's connection string>"
)

doc = '{ "_id":"book-102","type":"book", "name":"Horton hears a who 2","author":"Dr. Suess","published":"1953" }'

result = await hyper.data.add(doc)

```

## Examples

### How to add a document to hyper data?

```js
const doc = {
  id: "movie-1",
  type: "movie",
  title: "Dune",
  year: "2021",
};

const result = await hyper.data.add(doc);
console.log(result); // {ok: true, id: "movie-1"}
```

### How to get all the documents of type 'movie'?

```js
const result = await hyper.data.query({ type: "movie" });
console.log(result); // {ok: true, docs: [...]}
```

### How to add a cache key/value pair to hyper cache?

```js
const result = await hyper.cache.add("key", { counter: 1 });
console.log(result); // {ok: true}
```

## Documentation

hyper is a suite of service apis, with hyper connect you can specify the API you
want to connect with and the action you want to perform.
hyper.[service].[action] - with each service there are a different set of
actions to call. This table breaks down the service and action with description
of the action.

### data

| Service | Action | Description                                                         |
| ------- | ------ | ------------------------------------------------------------------- |
| data    | add    | creates a json document in the hyper data store                     |
| data    | list   | lists the documents given a start,stop,limit range                  |
| data    | get    | retrieves a document by id                                          |
| data    | update | updates a given document by id                                      |
| data    | remove | removes a document from the store                                   |
| data    | query  | queries the store for a set of documents based on selector criteria |
| data    | index  | creates an index for the data store                                 |
| data    | bulk   | inserts, updates, and removed document via a batch of documents     |

### cache

| Service | Action | Description                                                         |
| ------- | ------ | ------------------------------------------------------------------- |
| cache   | add    | creates a json document in the hyper cache store with a key         |
| cache   | get    | retrieves a document by key                                         |
| cache   | set    | sets a given document by key                                        |
| cache   | remove | removes a document from the cache                                   |
| cache   | query  | queries the cache for a set of documents based on a pattern matcher |

### search

| Service | Action | Description                                       |
| ------- | ------ | ------------------------------------------------- |
| search  | add    | indexes a json document in the hyper search index |
| search  | get    | retrieves a document from index                   |
| search  | remove | removes a document from the index                 |
| search  | query  | searches index by text                            |
| search  | load   | loads a batch of documents                        |

### storage

| Service | Action   | Description                              |
| ------- | -------- | ---------------------------------------- |
| storage | upload   | adds object/file to hyper storage bucket |
| storage | download | retrieves a object/file from bucket      |
| storage | remove   | removes a object/file from the bucket    |

### queue

| Service | Action  | Description                                                |
| ------- | ------- | ---------------------------------------------------------- |
| queue   | enqueue | posts object to queue                                      |
| queue   | errors  | gets list of errors occured with queue                     |
| queue   | queued  | gets list of objects that are queued and ready to be sent. |

---

### COMING SOON: Verify Signature

hyper Queue allows you to create a target web hook endpoint to receive jobs, in
order to secure that endpoint to only receive jobs from hyper, you can implement
a secret, this secret using sha256 to encode a `nounce` timestamp and a
signature of the job payload. We created a function on `hyper_connect` to make
it easier to implement your own middleware to validate these incoming jobs in a
secure way.



## Contributing

###Developer Setup

We prefer you use Gitpod.  Gitpod provides a fully initialized, perfectly set-up developer environmments the hyper connect SDK.

> We recommend you [install the Gitpod browser extension](https://www.gitpod.io/docs/browser-extension) to make this a one-click operation.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/tripott/hyper-connect-py-test)


### Static type checking and code formatting

We use git pre-commit hooks, black, and isort to prettify the code and run static type checking with mypy.   See the **.pre-commit-config.yaml**.

To run these checks, execute the `bash lint.sh` command or run the `bash .git/hooks/pre-commit` command in a terminal window where the virtual environment has been activated.

### Tests

Run the `bash test.sh` command or run `python -m unittest discover -s tests -v` in a terminal window where the virtual environment has been activated.

### Test Client

**sandbox.py** contains a quick and dirty client that takes hyper connect for. a test drive.  The `data_add` function attempts to add a book document to the hyper data service, while `data_get` retrieves a book by the doc `_id` primary key value.

```
$ pyton
>>> from sandbox import data_add, data_get
>>> import asyncio
>>> asyncio.run(data_add('{ "_id":"book-102","type":"book", "name":"Horton hears a who 2","author":"Dr. Suess","published":"1953" }'))
```

### License

Apache 2.0
