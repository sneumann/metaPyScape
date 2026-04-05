# coding: utf-8
"""mtbsccli - MetaboScape command-line client.

Usage examples
--------------
  # Configuration
  mtbsccli config set-server http://192.168.1.10/cxf/metaboscape
  mtbsccli config set-key          # prompts securely; never echoes key
  mtbsccli config show

  # Read-only data access
  mtbsccli get projects
  mtbsccli get project <projectId>
  mtbsccli get project-info <projectId>
  mtbsccli get featuretable <featureTableId>
  mtbsccli get feature <featureId>
  mtbsccli get samples <featureTableId>
  mtbsccli get intensity-matrix <featureTableId>
  mtbsccli get spectra <featureId>
  mtbsccli get msms <featureId>
  mtbsccli get eics <featureId>
  mtbsccli get eims <featureId>
  mtbsccli get ccs-models
  mtbsccli get annotation-config <configId>
  mtbsccli get annotation-methods <toolId>

Global flags
-------------
  --server / -s    Override server URL (or set env MTBSC_SERVER)
  --output / -o    Output format: table (default), json, yaml
"""

from __future__ import annotations

import getpass
import os
import sys
from typing import Optional

import click

import metaPyScape
from metaPyScape.rest import ApiException

from . import config as cfg
from . import output as out


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_client(server: Optional[str]) -> metaPyScape.ApiClient:
    """Build a configured ApiClient, exiting on missing credentials."""
    url = server or cfg.get_server_url()
    if not url:
        click.echo(
            "Error: No server URL configured.\n"
            "Run:  mtbsccli config set-server <url>\n"
            "  or  export MTBSC_SERVER=<url>",
            err=True,
        )
        sys.exit(1)

    api_key = cfg.get_api_key(prompt_if_missing=True)
    if not api_key:
        click.echo(
            "Error: No API key available.\n"
            f"  export {cfg.API_KEY_ENV}=<key>\n"
            "  or run:  mtbsccli config set-key",
            err=True,
        )
        sys.exit(1)

    configuration = metaPyScape.Configuration()
    configuration.host = url
    return metaPyScape.ApiClient(
        configuration=configuration,
        header_name="api-key",
        header_value=api_key,
    )


def _handle_api_error(exc: ApiException) -> None:
    click.echo(f"API error {exc.status}: {exc.reason}", err=True)
    if exc.body:
        click.echo(exc.body, err=True)
    sys.exit(1)


def _handle_connection_error(exc: Exception) -> None:
    click.echo(f"Connection error: {exc}", err=True)
    sys.exit(1)


def _call(fn, *args, **kwargs):
    """Call an API method and handle errors uniformly."""
    try:
        return fn(*args, **kwargs)
    except ApiException as exc:
        _handle_api_error(exc)
    except Exception as exc:  # noqa: BLE001
        _handle_connection_error(exc)


# ---------------------------------------------------------------------------
# Root command group
# ---------------------------------------------------------------------------


@click.group()
@click.option(
    "--server",
    "-s",
    envvar=cfg.SERVER_URL_ENV,
    metavar="URL",
    help="MetaboScape server base URL (overrides config / env MTBSC_SERVER).",
)
@click.option(
    "--output",
    "-o",
    type=click.Choice(["table", "json", "yaml"]),
    default="table",
    show_default=True,
    help="Output format.",
)
@click.version_option(package_name="metaPyScape", prog_name="mtbsccli")
@click.pass_context
def cli(ctx: click.Context, server: Optional[str], output: str) -> None:
    """mtbsccli – read-only command-line client for MetaboScape."""
    ctx.ensure_object(dict)
    ctx.obj["server"] = server
    ctx.obj["output"] = output


# ---------------------------------------------------------------------------
# config subcommands
# ---------------------------------------------------------------------------


@cli.group("config")
def config_group() -> None:
    """Manage mtbsccli configuration."""


@config_group.command("set-server")
@click.argument("url")
def config_set_server(url: str) -> None:
    """Set the MetaboScape server URL and save it to the config file."""
    conf = cfg.load_config()
    conf["server"] = url
    cfg.save_config(conf)
    click.echo(f"Server URL saved: {url}")


@config_group.command("set-key")
def config_set_key() -> None:
    """Securely store the API key in the config file (owner-read-only, 600)."""
    try:
        key = getpass.getpass("MetaboScape API Key: ")
    except (KeyboardInterrupt, EOFError):
        click.echo("\nAborted.", err=True)
        sys.exit(1)

    if not key:
        click.echo("No key entered – nothing saved.", err=True)
        sys.exit(1)

    conf = cfg.load_config()
    conf["api_key"] = key
    cfg.save_config(conf)
    click.echo(f"API key saved to {cfg.CONFIG_FILE} (permissions 600).")
    click.echo(
        f"Tip: you can also export {cfg.API_KEY_ENV}=<key> to avoid writing to disk."
    )


@config_group.command("show")
def config_show() -> None:
    """Display current configuration (API key is masked)."""
    conf = cfg.load_config()

    masked = dict(conf)
    raw_key = masked.get("api_key", "")
    if raw_key:
        masked["api_key"] = ("*" * max(0, len(raw_key) - 4)) + raw_key[-4:]

    click.echo(f"Config file : {cfg.CONFIG_FILE}")
    click.echo(f"  exists    : {cfg.CONFIG_FILE.exists()}")
    for k, v in masked.items():
        click.echo(f"  {k}: {v}")

    env_key = os.environ.get(cfg.API_KEY_ENV, "")
    if env_key:
        click.echo(
            f"  {cfg.API_KEY_ENV} (env): {'*' * max(0, len(env_key) - 4)}{env_key[-4:]}"
        )
    else:
        click.echo(f"  {cfg.API_KEY_ENV} (env): <not set>")


# ---------------------------------------------------------------------------
# get subcommands
# ---------------------------------------------------------------------------


@cli.group("get")
def get_group() -> None:
    """Retrieve one or many resources from MetaboScape."""


# -- projects ----------------------------------------------------------------


@get_group.command("projects")
@click.pass_context
def get_projects(ctx: click.Context) -> None:
    """List all projects."""
    client = _make_client(ctx.obj["server"])
    result = _call(metaPyScape.ProjectsApi(client).list_all_projects)
    out.format_output(result, ctx.obj["output"])


@get_group.command("project")
@click.argument("project_id")
@click.pass_context
def get_project(ctx: click.Context, project_id: str) -> None:
    """Get a project by PROJECT_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(metaPyScape.ProjectsApi(client).retrieve_project, project_id)
    out.format_output(result, ctx.obj["output"])


@get_group.command("project-info")
@click.argument("project_id")
@click.pass_context
def get_project_info(ctx: click.Context, project_id: str) -> None:
    """Get detailed task/workflow info for a project by PROJECT_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(metaPyScape.ProjectsApi(client).retrieve_project_info, project_id)
    out.format_output(result, ctx.obj["output"])


# -- feature tables ----------------------------------------------------------


@get_group.command("featuretable")
@click.argument("featuretable_id")
@click.pass_context
def get_featuretable(ctx: click.Context, featuretable_id: str) -> None:
    """Get a feature table by FEATURETABLE_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(
        metaPyScape.FeaturetableApi(client).retrieve_feature_table, featuretable_id
    )
    out.format_output(result, ctx.obj["output"])


# -- features ----------------------------------------------------------------


@get_group.command("feature")
@click.argument("feature_id")
@click.pass_context
def get_feature(ctx: click.Context, feature_id: str) -> None:
    """Get a single feature by FEATURE_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(metaPyScape.FeaturetableApi(client).retrieve_feature, feature_id)
    out.format_output(result, ctx.obj["output"])


@get_group.command("spectra")
@click.argument("feature_id")
@click.pass_context
def get_spectra(ctx: click.Context, feature_id: str) -> None:
    """Get MS ion spectra for a feature by FEATURE_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(
        metaPyScape.FeaturetableApi(client).retrieve_feature_ion_ms_spectra, feature_id
    )
    out.format_output(result, ctx.obj["output"])


@get_group.command("msms")
@click.argument("feature_id")
@click.pass_context
def get_msms(ctx: click.Context, feature_id: str) -> None:
    """Get MS/MS spectra for a feature by FEATURE_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(
        metaPyScape.FeaturetableApi(client).retrieve_feature_ms_ms_spectra, feature_id
    )
    out.format_output(result, ctx.obj["output"])


@get_group.command("msms-deiso")
@click.argument("feature_id")
@click.pass_context
def get_msms_deiso(ctx: click.Context, feature_id: str) -> None:
    """Get deisotoped MS/MS spectra for a feature by FEATURE_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(
        metaPyScape.FeaturetableApi(client).retrieve_feature_ms_ms_spectra_deiso,
        feature_id,
    )
    out.format_output(result, ctx.obj["output"])


@get_group.command("spectra-details")
@click.argument("feature_id")
@click.pass_context
def get_spectra_details(ctx: click.Context, feature_id: str) -> None:
    """Get detailed MS spectrum information for a feature by FEATURE_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(
        metaPyScape.FeaturetableApi(client).retrieve_feature_ms_spectra_details,
        feature_id,
    )
    out.format_output(result, ctx.obj["output"])


@get_group.command("eics")
@click.argument("feature_id")
@click.pass_context
def get_eics(ctx: click.Context, feature_id: str) -> None:
    """Get Extracted Ion Chromatograms (EICs) for a feature by FEATURE_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(
        metaPyScape.FeaturetableApi(client).retrieve_eics_for_feature, feature_id
    )
    out.format_output(result, ctx.obj["output"])


@get_group.command("eims")
@click.argument("feature_id")
@click.pass_context
def get_eims(ctx: click.Context, feature_id: str) -> None:
    """Get Extracted Ion Mobilograms (EIMs) for a feature by FEATURE_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(
        metaPyScape.FeaturetableApi(client).retrieve_eims_for_feature, feature_id
    )
    out.format_output(result, ctx.obj["output"])


# -- samples -----------------------------------------------------------------


@get_group.command("samples")
@click.argument("featuretable_id")
@click.pass_context
def get_samples(ctx: click.Context, featuretable_id: str) -> None:
    """List all samples for a feature table by FEATURETABLE_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(metaPyScape.SamplesApi(client).list_all_samples, featuretable_id)
    out.format_output(result, ctx.obj["output"])


# -- intensity matrix --------------------------------------------------------


@get_group.command("intensity-matrix")
@click.argument("featuretable_id")
@click.pass_context
def get_intensity_matrix(ctx: click.Context, featuretable_id: str) -> None:
    """Get the intensity matrix for a feature table by FEATURETABLE_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(
        metaPyScape.FeaturetableApi(client).retrieve_intensity_matrix, featuretable_id
    )
    out.format_output(result, ctx.obj["output"])


# -- CCS prediction ----------------------------------------------------------


@get_group.command("ccs-models")
@click.pass_context
def get_ccs_models(ctx: click.Context) -> None:
    """List available CCS prediction models."""
    client = _make_client(ctx.obj["server"])
    result = _call(metaPyScape.CcspredictApi(client).list_ccs_predict_models)
    out.format_output(result, ctx.obj["output"])


# -- annotations -------------------------------------------------------------


@get_group.command("annotation-config")
@click.argument("config_id")
@click.pass_context
def get_annotation_config(ctx: click.Context, config_id: str) -> None:
    """Get an annotation configuration by CONFIG_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(
        metaPyScape.FeaturetableApi(client).retrieve_annotation_configuration_by_id,
        config_id,
    )
    out.format_output(result, ctx.obj["output"])


@get_group.command("annotation-methods")
@click.argument("tool_id")
@click.pass_context
def get_annotation_methods(ctx: click.Context, tool_id: str) -> None:
    """List annotation methods for a given annotation tool by TOOL_ID."""
    client = _make_client(ctx.obj["server"])
    result = _call(
        metaPyScape.FeaturetableApi(client).retrieve_annotation_methods_by_tool_id,
        tool_id,
    )
    out.format_output(result, ctx.obj["output"])


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
