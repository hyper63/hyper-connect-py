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

Once you've created an environment variable named `HYPER` with a connection string, you're ready to make a call to the `connect` function which returns a `Hyper` object.

```py
from typing import Dict
from hyper_connect import connect
from hyper_connect.types import Hyper
from dotenv import dotenv_values

config = dotenv_values("./.env")

connection_string: str = str(config["HYPER"])
hyper: Hyper = connect(connection_string)

async def data_add():

        movie: Dict = {
            "_id": "movie-4000",
            "type": "movie",
            "title": "Back to the Future",
            "year": "1985",
        }

        result = await hyper.data.add(movie)

        print('hyper.data.add result --> ', result)
        # hyper.data.add result -->  {'id': 'movie-4000', 'ok': True, 'status': 201}
```

## Examples

### How to add a document to a hyper data service?

```py
from typing import Dict
from hyper_connect import connect
from hyper_connect.types import Hyper
from dotenv import dotenv_values

config = dotenv_values("./.env")

connection_string: str = str(config["HYPER"])
hyper: Hyper = connect(connection_string)

async def data_add():

        movie: Dict = {
            "_id": "movie-4000",
            "type": "movie",
            "title": "Back to the Future",
            "year": "1985",
        }

        result = await hyper.data.add(movie)

        print('hyper.data.add result --> ', result)
        # hyper.data.add result -->  {'id': 'movie-4000', 'ok': True, 'status': 201}
```
### How do I remove a doc from the data service?

```py
id: str = "movie-4000"
result = await hyper.data.remove(id)
print('hyper.data.remove result --> ', result)
# hyper.data.remove result -->  {'id': 'movie-4000', 'ok': True, 'status': 200}
```

### How do I get a doc from the data service?

```py
id: str = "book-000200"
result = await hyper.data.get(id)
print("hyper.data.get result --> ", result)

# hyper.data.get result -->  {'_id': 'book-000200', 'type': 'book', 'name': 'Tales of the South Pacific', 'author': 'James A. Michener', 'published': '1947', 'status': 200}
```

### What if a doc isn't found?

```py
id: str = "movie-105"
result = await hyper.data.get(id)
print("hyper.data.get result --> ", result)

# hyper.data.get result -->  {'ok': False, 'status': 404, 'msg': 'doc not found'}
```

### How do I update a doc within the data service?

```py
book: Dict = {
        "_id": "book-000100",
        "type": "book",
        "name": "The Lorax 100",
        "author": "Dr. Suess",
        "published": "1969",
    }

result = await hyper.data.update("book-000100", book)
print("hyper.data.update result --> ", result)
# hyper.data.update result -->  {'ok': True, 'id': 'book-000100', 'status': 200}
```

### How do I get a range of documents from the data service?

```py
from hyper_connect.types import Hyper, ListOptions

options: ListOptions = {
        "startkey": "book-000105",
        "limit": None,
        "endkey": "book-000106",
        "keys": None,
        "descending": None,
    }

result = await hyper.data.list(options)
print("hyper.data.list result --> ", result)
# hyper.data.list result -->  {'docs': [{...}, {...}], 'ok': True, 'status': 200}
```

### How do I retrieve a specific set of docs from the data service?

```py
options: ListOptions = {
        "startkey": None,
        "limit": None,
        "endkey": None,
        "keys": ["book-000105", "book-000106"],
        "descending": None,
    }

result = await hyper.data.list(options)
print("hyper.data.list result --> ", result)
# hyper.data.update result -->  {'docs': [{...}, {...}], 'ok': True, 'status': 200}

```


### How do I query for just books?

This example uses a `selector` to filter book documents.  An array of `fields` allows you to select which fields to return.  Use `limit` to restrict the number of documents returned.  This is helpful for pagination use cases.

```py
from hyper_connect.types import Hyper, QueryOptions

selector = {"type": "book"}

options: QueryOptions = {
    "fields": ["_id", "name", "published"],
    "sort": None,
    "limit": 3,
    "useIndex": None,
}

result = await hyper.data.query(selector, options)
print("hyper.data.query result --> ", result)

# hyper.data.query result -->  {'docs': [{'_id': 'book-000010', 'name': 'The Lorax', 'published': '1959'}, {'_id': 'book-000020', 'name': 'The Lumberjack named Lorax the tree slayer', 'published': '1969'}, {'_id': 'book-000100', 'name': 'The Lorax 100', 'published': '1969'}], 'ok': True, 'status': 200}
```


here

### How do I sort data from my data service?

First create an index on the fields you wish to sort.  Then use the `QueryOptions` with the `sort` key to sort.

```py
index_result = await hyper.data.index(
        "idx_author_published", ["author", "published"]
)

print('index_result --> ', index_result )

selector = {"type": "book", "author": "James A. Michener"}

options: QueryOptions = {
    "fields": ["author", "published"],
    "sort": [{"author": "DESC"}, {"published": "DESC"}],
    "useIndex": "idx_author_published",
}

result = await hyper.data.query(selector, options)
print("hyper.data.query result --> ", result)

# index_result -->  {'ok': True, 'status': 201}

# hyper.data.query result -->  {'docs': [{'author': 'James A. Michener', 'published': '1985'}, {'author': 'James A. Michener', 'published': '1959'}, {'author': 'James A. Michener', 'published': '1947'}], 'ok': True, 'status': 200}
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

### Developer Setup

We prefer you use Gitpod.  Gitpod provides a fully initialized, perfectly set-up developer environmments the hyper connect SDK.

> We recommend you [install the Gitpod browser extension](https://www.gitpod.io/docs/browser-extension) to make this a one-click operation.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/tripott/hyper-connect-py-test)

### Environment Variables

If you plan on running tests, you'll need to create an environment variable named `HYPER`.

- Create a **.env** file in the project root.
- Within **.env**, create an environment variable named `HYPER` with a value of your hyper app's [connection string](https://docs.hyper.io/app-keys#nq-connection-string).


```bash
HYPER=cloud://your app key:your app secret--gI1MkcrUqFPMR@cloud.hyper.io/express-quickstart
```

## Linting

We use git pre-commit hooks, black, and isort to prettify the code and run static type checking with mypy.   See the **.pre-commit-config.yaml**.

To run these checks, execute the `make lint` command.

## Tests

> Heads up! Integration tests assume a hyper app and services have been created.  See https://docs.hyper.io/applications for details on creating hyper applications and service.

A storage service should have the following configuration:

![Search Service Config](search-svc-config.png)

Run the `make test` script to run the unit and integration tests.

### License

Apache 2.0
