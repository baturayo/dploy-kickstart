## dploy-kickstart

[![codecov](https://codecov.io/gh/dploy-ai/dploy-kickstart/branch/master/graph/badge.svg?token=KypiVRoPJz)](https://codecov.io/gh/dploy-ai/dploy-kickstart)

Expose your Python functions via an HTTP API.

### Installation

`pip install dploy_kickstart`

When installed it provides a `kickstart` executable. Have a look at the help functionality: `kickstart --help`.


### Usage

`dploy_kickstart` is a helper utility that can expose your Python functions as HTTP endpoints. Based on comment annotations it wraps your chosen functions to be served as API endpoints.

Let's say you have a `script.py` with `@dploy` comment annotations:

```python
# @dploy endpoint echo
def echo_func(payload):
    return payload
```

Serve this function with:

```sh
kickstart serve -e script.py
```

Let's try to call the endpoint via `curl`.

```
$ curl -d '{"foo":"bar"}' -H "Content-Type: application/json" -X POST http://localhost:8080/echo/

{"foo":"bar"}
```

### Annotations

Following annotation options are currently available.


`# @dploy endpoint {endpoint_path}`
> Will expose the annotated function on path {endpoint_path} with trailing slash (and redirect without trailing slash).

`# @dploy response_mime_type {mimetype}`

> Specify response mime type, will wrap function response accordingly.

default: `application/json`

available: 
- `application/json`

`# @dploy request_content_type {content_type}`
> Specify allowed request content type.

default: application/json

available:
- application/json

`# @dploy request_method {method}`
> Specify allowed request method.

default: `post`

available: any method supported by Flask

`# @dploy json_to_kwargs`

> Will map json payload's keys to function kwargs if supplied.

### Endpoint utilities

Following paths are generated automatically:

- `GET /healthz`: that always returns a 200
- `GET /openapi.yaml`: autogenerated OpenAPI Spec (WIP)

### Current dependency tree

Aim is to keep this as small as possible to not clutter the user space.

```
$ poetry show --no-dev --tree

apispec 3.3.0 A pluggable API specification generator. Currently supports the OpenAPI Specification (f.k.a. the Swagger specification).
click 7.1.2 Composable command line interface toolkit
flask 1.1.2 A simple framework for building complex web applications.
├── click >=5.1
├── itsdangerous >=0.24
├── jinja2 >=2.10.1
│   └── markupsafe >=0.23 
└── werkzeug >=0.15
paste 3.4.0 Tools for using a Web Server Gateway Interface stack
└── six >=1.4.0
waitress 1.4.3 Waitress WSGI server
```