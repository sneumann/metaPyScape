# coding: utf-8
"""Configuration management for mtbsccli.

Credential resolution order (highest to lowest priority):
  1. Environment variable MTBSC_API_KEY
  2. Config file  ~/.config/mtbsccli/config.yml  (permissions 600)
  3. Interactive prompt via getpass (if allowed)
"""

from __future__ import annotations

import getpass
import os
import stat
from pathlib import Path

import yaml

CONFIG_DIR = Path.home() / ".config" / "mtbsccli"
CONFIG_FILE = CONFIG_DIR / "config.yml"
API_KEY_ENV = "MTBSC_API_KEY"
SERVER_URL_ENV = "MTBSC_SERVER"


def load_config() -> dict:
    """Load configuration from the user config file."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as fh:
            return yaml.safe_load(fh) or {}
    return {}


def save_config(conf: dict) -> None:
    """Save configuration to the user config file with owner-only permissions."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as fh:
        yaml.dump(conf, fh, default_flow_style=False)
    # Restrict to owner read/write only (600)
    os.chmod(CONFIG_FILE, stat.S_IRUSR | stat.S_IWUSR)


def get_api_key(prompt_if_missing: bool = True) -> str | None:
    """Return the API key from the first available source.

    Sources checked in order:
      1. Environment variable MTBSC_API_KEY
      2. Config file api_key field
      3. Interactive prompt (if *prompt_if_missing* is True)
    """
    # 1. Environment variable
    key = os.environ.get(API_KEY_ENV)
    if key:
        return key

    # 2. Config file
    conf = load_config()
    key = conf.get("api_key")
    if key:
        return key

    # 3. Interactive prompt
    if prompt_if_missing:
        try:
            key = getpass.getpass("MetaboScape API Key: ")
            return key if key else None
        except (KeyboardInterrupt, EOFError):
            return None

    return None


def get_server_url() -> str | None:
    """Return the server URL from env var or config file."""
    url = os.environ.get(SERVER_URL_ENV)
    if url:
        return url
    conf = load_config()
    return conf.get("server")
