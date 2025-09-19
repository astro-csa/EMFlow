from __future__ import annotations

import json
from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any

from emsoft.common.emsoft_config import EMSoftConfig

_DEFAULTS_ROOT = Path.home() / ".config" / "EMsoft" / "defaults"


def get_program_defaults_path(experiment_name: str, program_name: str) -> Path:
    """Return the file path storing defaults for the given experiment/program."""

    return _DEFAULTS_ROOT / experiment_name / f"{program_name}.json"


def save_defaults(experiment_name: str, program_name: str, config: EMSoftConfig) -> Path:
    """Persist the provided configuration to the defaults location."""

    path = get_program_defaults_path(experiment_name, program_name)
    config.save(path)
    return path


def load_defaults(
    experiment_name: str,
    program_name: str,
    config_type: type[EMSoftConfig],
) -> EMSoftConfig | None:
    """Load defaults if they exist, returning a populated config instance."""

    path = get_program_defaults_path(experiment_name, program_name)
    if not path.exists():
        return None

    try:
        with path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None

    try:
        return _build_dataclass(config_type, raw)
    except Exception:
        return None


def _build_dataclass(dataclass_type: type[EMSoftConfig], data: dict[str, Any]) -> EMSoftConfig:
    kwargs: dict[str, Any] = {}

    for field in fields(dataclass_type):
        if not field.init:
            continue

        if field.name not in data:
            continue

        value = data[field.name]
        if value is None:
            continue

        nested = _resolve_dataclass_type(field.type)
        if nested and isinstance(value, dict):
            kwargs[field.name] = _build_dataclass(nested, value)
        else:
            kwargs[field.name] = value

    return dataclass_type(**kwargs)


def _resolve_dataclass_type(field_type: Any) -> type | None:
    if isinstance(field_type, type) and is_dataclass(field_type):
        return field_type

    origin = getattr(field_type, "__origin__", None)
    if not origin:
        return None

    for arg in getattr(field_type, "__args__", []):
        if isinstance(arg, type) and is_dataclass(arg):
            return arg

    return None
