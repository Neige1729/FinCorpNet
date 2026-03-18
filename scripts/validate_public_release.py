#!/usr/bin/env python3
from __future__ import annotations

import json

from public_release_tools import default_paths, validate_release


def main() -> int:
    paths = default_paths()
    result = validate_release(paths["manifest"], paths["checksums"])
    print(json.dumps(result, indent=2))
    ok = (
        not result["missing"]
        and not result["checksum_errors"]
        and not any(result["ownership_errors"].values())
        and not any(result["aux_errors"].values())
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
