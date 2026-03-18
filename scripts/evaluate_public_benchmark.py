#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from public_release_tools import (
    evaluate_task_a,
    evaluate_task_b,
    iter_csv_rows,
    read_jsonl,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a public benchmark submission against released references.")
    parser.add_argument("--task", required=True, choices=["task_a", "task_b"])
    parser.add_argument("--submission", required=True)
    parser.add_argument("--references", required=True)
    parser.add_argument("--edges", required=True)
    args = parser.parse_args()

    submission = read_jsonl(args.submission)
    references = read_jsonl(args.references)
    edges = list(iter_csv_rows(args.edges))
    result = evaluate_task_a(submission, references, edges) if args.task == "task_a" else evaluate_task_b(submission, references, edges)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
