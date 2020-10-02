"""Flask server logic."""

import logging
import typing
from fastapi import FastAPI, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import dploy_kickstart.wrapper as pw
import dploy_kickstart.errors as pe

log = logging.getLogger(__name__)


def append_entrypoint(app: FastAPI, entrypoint: str, location: str) -> FastAPI:
    """Add routes/functions defined in entrypoint."""
    mod = pw.import_entrypoint(entrypoint, location)
    fm = pw.get_func_annotations(mod)

    if not any([e.endpoint for e in fm]):
        raise Exception("no endpoints defined")

    api_router = APIRouter()

    # iterate over annotations in usercode
    for f in fm:
        if f.endpoint:
            log.debug(
                f"adding endpoint for func: {f.__name__} (func_args: {f.comment_args})"
            )

            api_router.add_api_route(
                methods=[f.request_method.upper()],
                path=f.endpoint_path,
                endpoint=pw.func_wrapper(f),
            )

    app.include_router(api_router)
    return app


def generate_app() -> typing.Generic:
    """Generate a FastApi app."""
    app = FastAPI()

    @app.get("/healthz/", status_code=200)
    async def health_check() -> None:
        return "healthy"

    @app.exception_handler(pe.ServerException)
    async def handle_server_exception(_, exc: pe.ServerException) -> None:
        response = jsonable_encoder(exc)
        return JSONResponse(status_code=exc.status_code, content=response)

    return app
