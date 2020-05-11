import logging
import typing

from flask import Flask, jsonify

import dploy_kickstart.wrapper as pw
import dploy_kickstart.errors as pe
import dploy_kickstart.openapi as po

log = logging.getLogger(__name__)


def append_entrypoint(
    app: typing.Generic, entrypoint: str, location: str
) -> typing.Generic:
    """Add routes/functions defined in entrypoint."""
    mod = pw.import_entrypoint(entrypoint, location)
    fm = pw.get_func_annotations(mod)

    if len(list(filter(lambda e: e.endpoint, fm))) == 0:
        raise Exception("no endpoints defined")

    openapi_spec = po.base_spec(title=entrypoint)
    # iterate over annotations in usercode
    # only add /predict endpoint
    for f in fm:
        if f.endpoint:
            log.debug(
                "adding endpoint for func: {} (func_args: {})".format(
                    f.__name__, f.comment_args
                )
            )

            app.add_url_rule(
                f.endpoint_path,
                f.endpoint_path,
                pw.func_wrapper(f),
                methods=[f.endpoint_method],
            )

            # add info about endpoint to api spec
            po.path_spec(openapi_spec, f)

    app.add_url_rule(
        "/openapi.yaml", "/openapi.yaml", openapi_spec.to_yaml, methods=["GET"]
    )

    return app


def generate_app() -> typing.Generic:
    app = Flask(__name__)

    @app.route("/healthz/", methods=["GET"])
    def health_check() -> None:
        return "healthy", 200

    @app.errorhandler(pe.ServerException)
    def handle_server_exception(error: Exception) -> None:
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app