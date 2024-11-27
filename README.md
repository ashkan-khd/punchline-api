# General

This application implements a minimalistic flask API application that would let the user search, create, delete and
update jokes from [Chuck Norris jokes](https://api.chucknorris.io/), that works through for example Postman.
To simplify the description, we will call [Chuck Norris jokes](https://api.chucknorris.io/) as remote and application
implemented in this repository as local.

## The APIs

![](https://api.chucknorris.io/img/chucknorris_logo_coloured_small.png)

The API mainly consists of these 5 endpoints:

### `GET /jokes/?query={query}`

Free text search endpoint. You should take local and remote search results into consideration.

### `POST /api/jokes/`

Endpoint to create joke locally.

### `GET /api/jokes/{id}`

Endpoint to retrieve a joke by unique id. You should take local and remote results into consideration.

### `PUT /api/jokes/{id}`

Endpoint to update a joke by unique id. If the joke does not exist, return 404 not found. But if it does, store a
updated version locally. Any subsequent reads should only see this updated version.

### `DELETE /api/jokes/{id}`

Endpoint to delete a joke by unique id. If the joke does not exist, return 404 not found. But if it does, mark the joke
locally as deleted. Any subsequent reads should *NOT* see this joke.
