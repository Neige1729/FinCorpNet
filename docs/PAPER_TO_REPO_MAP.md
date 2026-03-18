# Paper To Repository Map

## Purpose

This note maps the public claims in the paper to concrete artifacts in the repository so that reviewers can quickly verify what is already released.

## Dataset schema and temporal semantics

- paper sections on data model and validity intervals
- repository artifacts: `DATA_CARD.md`, `docs/SCHEMA.md`, `scripts/public_stats.py`

## Snapshot-valid evidence protocol

- paper sections on snapshot-valid Task A / Task B evidence
- repository artifacts: `docs/BENCHMARKS.md`, `benchmarks/task_a_submission_schema.json`, `benchmarks/task_b_submission_schema.json`, `scripts/evaluate_public_benchmark.py`

## Public benchmark tier

- paper benchmark protocol mirrored as an anonymized public release tier
- repository artifacts: `benchmarks/public_release/`, `docs/MINI_BENCHMARK.md`, `scripts/validate_submission.py`

## Release validation and reproducibility scripts

- paper wording about released scripts that reproduce released tables or reported statistics
- repository artifacts: `scripts/validate_public_release.py`, `scripts/public_stats.py`, `REPRODUCIBILITY.md`

## Release boundary

- paper wording about a larger release remaining under post-publication review
- repository artifacts: `RELEASE_POLICY.md`, `docs/ARTIFACT_AVAILABILITY.md`
