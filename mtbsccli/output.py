# coding: utf-8
"""Output formatting helpers for mtbsccli."""

from __future__ import annotations

import json
import sys
from typing import Any

import yaml


def _to_serializable(obj: Any) -> Any:
    """Recursively convert API model objects to plain Python dicts/lists."""
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    if isinstance(obj, list):
        return [_to_serializable(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _to_serializable(v) for k, v in obj.items()}
    # Swagger-generated model objects expose a to_dict() method
    if hasattr(obj, "to_dict"):
        return _to_serializable(obj.to_dict())
    # Fallback: use public attributes
    if hasattr(obj, "__dict__"):
        return {
            k: _to_serializable(v)
            for k, v in obj.__dict__.items()
            if not k.startswith("_")
        }
    return str(obj)


def format_output(data: Any, output_format: str = "table") -> None:
    """Print *data* in the requested *output_format*.

    Writes only to stdout so that the output can be safely piped to tools
    like ``jq`` without extra lines contaminating the stream.
    """
    if output_format == "json":
        print(json.dumps(_to_serializable(data), indent=2, default=str), file=sys.stdout)
        sys.stdout.flush()
    elif output_format == "yaml":
        print(yaml.dump(_to_serializable(data), default_flow_style=False), end="")
    else:
        _print_table(data)


# ---------------------------------------------------------------------------
# Table rendering
# ---------------------------------------------------------------------------

_MAX_COL_WIDTH = 50


def _print_table(data: Any) -> None:
    if data is None:
        print("No data")
        return
    if isinstance(data, list):
        if not data:
            print("No items found.")
        else:
            _print_list_as_table(data)
    else:
        _print_object_as_kv(data)


def _print_list_as_table(items: list) -> None:
    """Render a list of model objects as an ASCII table."""
    dicts = [_to_serializable(item) for item in items]
    if not dicts or not isinstance(dicts[0], dict):
        for item in dicts:
            print(item)
        return

    # Collect ordered keys from the first item (preserve insertion order)
    keys = list(dicts[0].keys())
    # Compute column widths (capped)
    widths = {
        k: min(
            _MAX_COL_WIDTH,
            max(len(k), *(len(str(d.get(k, "") or "")) for d in dicts)),
        )
        for k in keys
    }

    header = "  ".join(k.upper().ljust(widths[k]) for k in keys)
    print(header)
    print("-" * len(header))
    for d in dicts:
        row = "  ".join(
            str(d.get(k, "") or "").ljust(widths[k])[: widths[k]] for k in keys
        )
        print(row)


def _print_object_as_kv(obj: Any, indent: int = 0) -> None:
    """Render a single model object as indented key: value lines.

    Nested dicts and lists of dicts are expanded recursively so that no
    raw Python repr strings (``[{'key': ...}]``) ever appear in the output.
    """
    prefix = "  " * indent
    d = _to_serializable(obj)
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, dict):
                print(f"{prefix}{k}:")
                _print_object_as_kv(v, indent + 1)
            elif isinstance(v, list):
                if not v:
                    print(f"{prefix}{k}: []")
                elif all(isinstance(item, dict) for item in v):
                    print(f"{prefix}{k}:")
                    for i, item in enumerate(v):
                        print(f"{prefix}  [{i}]")
                        _print_object_as_kv(item, indent + 2)
                else:
                    print(f"{prefix}{k}: {v}")
            else:
                print(f"{prefix}{k}: {v}")
    else:
        print(f"{prefix}{d}")
