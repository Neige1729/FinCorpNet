#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from public_release_tools import compute_public_stats, default_paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute public release summary statistics for a snapshot year.")
    parser.add_argument("--year", type=int, default=2025)
    args = parser.parse_args()

    paths = default_paths()
    result = compute_public_stats(
        entities_path=paths["entities"],
        ownership_path=paths["ownership"],
        aux_path=paths["aux"],
        year=args.year,
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
