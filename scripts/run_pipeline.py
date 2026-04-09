"""Backward-compatible wrapper for legacy script name."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

from finding_donors.pipeline import run_training_pipeline  # noqa: E402


def main() -> None:
    run_training_pipeline()


if __name__ == "__main__":
    main()
