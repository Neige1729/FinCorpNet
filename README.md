# FinCorpNet Public Release v0.3.0

FinCorpNet is a temporal corporate ownership graph for **snapshot-valid equity penetration analysis**. This upload bundle is the **anonymized public release subset** accompanying the KDD 2026 paper *FinCorpNet: A Large-Scale Temporal Corporate Ownership Graph for Equity Penetration Analysis*.

The released subset preserves the paper's public-facing schema and benchmark interface over a **China-centered registry and shareholding-filing corpus** while withholding source-native identifiers and names. The public release is approximately **1% of the paper-scale resource**:

- **584,000 entities**
- **3,227,000 temporal ownership edges**
- **1,561,000 auxiliary relations**
- **16,200 / 4,800 / 5,200 Task A targets** for train / val / test
- **784 / 269 / 287 Task B groups** for train / val / test

## Public Release At A Glance

- coverage years: **1990-2025**
- release tier: **anonymized public subset**
- bundle version: **v0.3.0**
- public identity surface: stable surrogate `entity_id` only
- ownership semantics carried only by `ownership_edges`
- benchmark assets released under `benchmarks/public_release/`
- slim public reproducibility scripts released under `scripts/`
- integrity material released under `metadata/`

## What This Upload Bundle Contains

### Data tables

- `data-public/entities/entities_public_1pct.csv`
- `data-public/ownership_edges/ownership_edges_public_1pct.csv`
- `data-public/aux_relations/aux_relations_public_1pct.csv`

`entities` publishes stable public IDs plus normalized attributes. `jurisdiction_code` is normalized to a release-safe public code space that includes PRC province-level codes together with a small set of offshore or special-region codes when they are part of the anonymized public export. `ownership_edges` is the authoritative table for shareholding semantics, validity intervals, and benchmark evidence. `aux_relations` carries contextual links that remain separate from ownership assertions.

### Benchmark interface

- `benchmarks/task_a_submission_schema.json`
- `benchmarks/task_b_submission_schema.json`
- `benchmarks/public_release/`

The public benchmark release contains chronological train / val / test files for Task A and Task B together with public reference outputs.

### Release metadata

- `metadata/public_release_summary.json`
- `metadata/anonymization_policy.md`
- `metadata/redaction_dictionary.csv`
- `metadata/flag_dictionary.csv`
- `metadata/public_release_manifest.csv`
- `metadata/checksums.sha256`

### Public reproducibility scripts

- `scripts/validate_public_release.py`
- `scripts/validate_submission.py`
- `scripts/public_stats.py`
- `scripts/evaluate_public_benchmark.py`

These scripts target Python `3.10+`.

## Verification

This upload bundle is meant to be **inspected and validated**, not used as an internal build workspace. To verify file integrity:

```bash
sha256sum -c metadata/checksums.sha256
```

To validate the bundle and recompute public-facing checks from the shipped files:

```bash
python scripts/validate_public_release.py
python scripts/public_stats.py --year 2025
```

The release validator checks manifest integrity, checksums, entity endpoints, date parsing, interval consistency, year-range compliance, and ownership-weight bounds on the shipped public tables.

The manifest at `metadata/public_release_manifest.csv` lists the files that belong to the release bundle and their row counts or byte sizes.

## Release Boundary

This public package does **not** redistribute:

- source-native identifiers
- source-native names or registration strings
- direct source-to-release mapping tables
- internal construction code or development-only tooling
- the full production-scale corpus described in the paper

The current upload is a public inspection, benchmark, and verification package. Expanded releases remain subject to source-distribution and compliance review following publication.

## Read First

- [`DATA_CARD.md`](DATA_CARD.md)
- [`RELEASE_POLICY.md`](RELEASE_POLICY.md)
- [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md)
- [`DATA_LICENSE.md`](DATA_LICENSE.md)
- [`docs/SCHEMA.md`](docs/SCHEMA.md)
- [`docs/BENCHMARKS.md`](docs/BENCHMARKS.md)
- [`docs/PAPER_TO_REPO_MAP.md`](docs/PAPER_TO_REPO_MAP.md)

## Citation

```bibtex
@inproceedings{shen2026fincorpnet,
  title={FinCorpNet: A Large-Scale Temporal Corporate Ownership Graph for Equity Penetration Analysis},
  author={Shen, Mingxuan and Hong, Liang and Xu, Qingying and Deng, Xiyue and Song, Baogang},
  booktitle={Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining},
  year={2026}
}
```

For machine-readable citation metadata, use [`CITATION.cff`](CITATION.cff).
