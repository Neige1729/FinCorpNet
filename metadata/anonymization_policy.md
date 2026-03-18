# Anonymization Policy

## Release goal

The public FinCorpNet release is distributed as an anonymized 1%-scale artifact intended for methodology research, benchmark validation, and reviewer-facing reproducibility. It preserves the paper's registry/shareholding/auxiliary schema while withholding source-native identifiers and strings, and it is released as a public subset rather than a direct redistribution of the full production corpus.

## Applied transformations

The public release applies the following transformations before publication:

1. Stable surrogate `entity_id` values replace source-native registry identifiers.
2. Entity names are omitted from the public `entities` table.
3. `jurisdiction_code` values are normalized to a release-safe public code space centered on PRC province-level codes, with limited offshore or special-region codes retained where needed by the anonymized export.
4. `prov` is collapsed to source-family level channels such as `registry_effective`, `registry_filing`, `annual_report`, and `exchange_filing`.
5. Temporal anchoring and ambiguity flags such as `date_from_filing`, `t_end_known`, `t_end_unknown`, `overlap_interval`, and `conflicting_events` are retained so downstream users can reproduce the paper's snapshot semantics.

## What is intentionally not released

The public repository does not expose:

- source-native identifiers
- direct source-to-release linkage tables
- raw source names or registration strings
- fine-grained provenance hooks that would reveal non-redistributable source internals

## Practical consequence

The public tables preserve graph structure, temporal semantics, normalized public attributes, and benchmark protocol compatibility, but they should not be interpreted as source-level entity disclosures.
