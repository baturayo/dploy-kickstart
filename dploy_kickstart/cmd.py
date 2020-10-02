"""CLI commands."""

import os
import logging

import click

from dploy_kickstart import deps as pd
from dploy_kickstart import server as ps
import uvicorn

log = logging.getLogger(__name__)


@click.group()
def cli() -> None:
    """CLI entrypoint."""
    pass


@cli.command(help="run dploy_kickstart server")
@click.option(
    "-e", "--entrypoint", required=True, help=".py or .ipynb to use as entrypoint"
)
@click.option(
    "-l",
    "--location",
    required=True,
    help="location of the script or notebook (and that will "
    + "be used as execution context)",
)
@click.option(
    "-d",
    "--deps",
    help="install dependencies; comma separated paths to either requirements.txt "
    + "or setup.py files. note that this can be run seperately via the "
    + "'install-deps' command",
)
@click.option(
    "--asgi/--no-asgi",
    default=True,
    help="Use ASGI server, defaults to True,"
    + " else launches a FastAPI debug server.",
)
@click.option(
    "-h", "--host", help="Host to serve on, defaults to '0.0.0.0'", default="0.0.0.0"
)
@click.option(
    "-p", "--port", help="Port to serve on, defaults to '8080'", default=8080, type=int
)
def serve(
    entrypoint: str, location: str, deps: str, asgi: bool, host: str, port: int
) -> None:
    """CLI serve."""
    if deps:
        click.echo(f"Installing deps: {deps}")
        _deps(deps, location)

    app = ps.generate_app()
    app = ps.append_entrypoint(app, entrypoint, os.path.abspath(location))

    uvicorn.run(
        app,
        host=os.getenv("DPLOY_KICKSTART_HOST", "0.0.0.0"),
        port=int(os.getenv("DPLOY_KICKSTART_PORT", 8080)),
    )


@cli.command(help="install dependencies")
@click.option(
    "-d",
    "--deps",
    required=True,
    help="comma separated paths to either requirements.txt" " or setup.py files",
)
@click.option(
    "-l",
    "--location",
    default=".",
    required=False,
    help="location of the script or notebook (and that will "
    + "be used as execution context). Will default to '.'",
)
def install_deps(deps: str, location: str) -> None:
    """CLI install dependencies."""
    click.echo(f"Installing deps... {deps}")
    _deps(deps, location)


def _deps(deps: str, location: str) -> None:
    """Install deps."""
    for r in deps.split(","):
        if not r:
            pass  # to allow to pass empty string when use in templated manner
        elif r.endswith("requirements.txt"):
            pd.install_requirements_txt(os.path.abspath(os.path.join(location, r)))
        elif r.endswith("setup.py"):
            pd.install_setup_py(os.path.abspath(os.path.join(location, r)))
        else:
            raise Exception(
                "unsupported dependency install defined: {}. "
                "Supported formats: "
                "requirements.txt, setup.py".format(r)
            )


if __name__ == "__main__":
    _entrypoint = "cbt_v2/deployment.py"
    _location = "/Users/baturayofluoglu/Workspace/ai-email-cbt-tfidf"
    _deps = False
    os.environ["LANGUAGE"] = "en"
    serve(_entrypoint, _location, _deps, asgi=True, host="0.0.0.0", port=80)
