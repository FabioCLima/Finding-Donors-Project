"""CLI entry point for training pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_ROOT))

from finding_donors.pipeline import run_training_pipeline  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Finding Donors training pipeline.")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to YAML config file (default: configs/base.yaml).",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default=None,
        help="Optional log level override (e.g., INFO, DEBUG).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_training_pipeline(config_path=args.config, log_level_override=args.log_level)


if __name__ == "__main__":
    main()

