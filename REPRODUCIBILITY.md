# Reproducibility Guide

## Scope

This guide documents what can be **verified directly** from the upload bundle. The upload package is a publication-facing release artifact with a slim reproducibility surface rather than a full internal build repository.

## Runtime

- Python `3.10+`

## What can be checked from this bundle

The upload bundle supports:

- manifest inspection via `metadata/public_release_manifest.csv`
- checksum verification via `metadata/checksums.sha256`
- schema inspection via `docs/SCHEMA.md`
- benchmark-interface inspection via `benchmarks/` and `docs/BENCHMARKS.md`
- release validation via `scripts/validate_public_release.py`
- public statistics recomputation via `scripts/public_stats.py`
- submission validation via `scripts/validate_submission.py`
- benchmark evaluation via `scripts/evaluate_public_benchmark.py`
- anonymization and release-boundary review via `metadata/anonymization_policy.md` and `RELEASE_POLICY.md`

## Recommended verification workflow

### 1. Verify file integrity

```bash
sha256sum -c metadata/checksums.sha256
```

### 2. Inspect release inventory

Review `metadata/public_release_manifest.csv` to confirm the bundle contains only the published data tables, benchmark assets, metadata, and release documentation.

### 3. Inspect schema and benchmark surface

Read:

- `docs/SCHEMA.md`
- `docs/BENCHMARKS.md`
- `docs/MINI_BENCHMARK.md`
- `benchmarks/task_a_submission_schema.json`
- `benchmarks/task_b_submission_schema.json`

### 4. Re-run public validation and statistics

```bash
python scripts/validate_public_release.py
python scripts/public_stats.py --year 2025
```

### 5. Inspect public references

The released benchmark files under `benchmarks/public_release/` provide the public train / val / test instances and reference outputs for the anonymized release tier.

## Practical note

This upload bundle intentionally omits internal generation code, development packaging, CI, and other private construction surfaces. It does include a slim set of public-facing scripts for validating the released files and reproducing release-level checks from the shipped public subset.

## Expanded post-publication release

The planned larger release may add:

- larger or full data tables
- expanded benchmark bundles
- additional provenance-safe metadata
- richer release governance material
