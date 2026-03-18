#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from public_release_tools import (
    read_jsonl,
    validate_task_a_submission,
    validate_task_b_submission,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a public benchmark submission against the released schemas and instance IDs.")
    parser.add_argument("--task", required=True, choices=["task_a", "task_b"])
    parser.add_argument("--submission", required=True)
    parser.add_argument("--instances", required=True)
    args = parser.parse_args()

    submission = read_jsonl(args.submission)
    instances = read_jsonl(args.instances)
    result = (
        validate_task_a_submission(submission, instances)
        if args.task == "task_a"
        else validate_task_b_submission(submission, instances)
    )
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
