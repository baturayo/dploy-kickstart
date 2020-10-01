"""Utilities to transform requests and responses."""

import typing
from fastapi import Response
import dploy_kickstart.annotations as da


def json_resp(func_result: typing.Any) -> Response:
    """Transform json response."""
    return func_result


def json_req(f: da.AnnotatedCallable, body: dict):
    """Preprocess application/json request."""
    if f.json_to_kwargs:
        return f(**body)
    else:
        return f(body)


MIME_TYPE_REQ_MAPPER = {
    "application/json": json_req,
}

MIME_TYPE_RES_MAPPER = {
    "application/json": json_resp,
}
