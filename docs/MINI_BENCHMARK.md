# Public Benchmark Tiers

## Purpose

The repository exposes the `public_release` benchmark tier for the anonymized 1%-scale release.

This public release tier is the benchmark surface that corresponds most closely to the paper's public protocol.

## Split design

The public release benchmark follows the paper's chronological split logic:

- `train`: 2015-2021
- `val`: 2022-2023
- `test`: 2024-2025

## Task A assets

For each split, the repository releases:

- `task_a_instances_<split>.jsonl`
- `task_a_references_<split>.jsonl`

Each Task A instance contains:

- `year`
- `target`
- `candidate_set`
- `instance_id`

## Task B assets

For each split, the repository releases:

- `task_b_instances_<split>.jsonl`
- `task_b_references_<split>.jsonl`

Each Task B instance defines a yearly universe. Each reference defines:

- groups
- witness edges
- the same yearly snapshot semantics used by Task A

## Intended use

The public release benchmark is intended for:

- inspecting the public benchmark payload structure
- validating evidence-path / witness-subgraph behavior
- reviewer-oriented reproducibility on a release-scale artifact
- rerunning the slim public evaluation and validation scripts shipped in `scripts/`

It is not the full benchmark scale reported in the paper, but it is large enough to support release-scale validation and benchmark runs.
