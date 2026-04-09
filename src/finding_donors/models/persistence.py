"""Persistence helpers for artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np


def _to_jsonable(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, tuple):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, np.generic):
        return value.item()
    return str(value)


def save_model(model: object, path: Path) -> None:
    """Persist trained model to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def save_json(payload: dict[str, Any], path: Path) -> None:
    """Persist metadata to JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = _to_jsonable(payload)
    with path.open("w", encoding="utf-8") as file:
        json.dump(serialized, file, indent=2, ensure_ascii=False)

