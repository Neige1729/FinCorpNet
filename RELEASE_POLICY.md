# Release Policy

## Why the repository uses staged release wording

FinCorpNet is intended to be a long-lived dataset and benchmark resource. Some fields, identifiers, provenance hooks, and benchmark artifacts remain tied to redistribution review. To stay precise about what is public today versus what remains under review, the repository follows a **two-stage release policy**.

## Stage 1: anonymized public release available now

The current public repository contains:

- schema and field-level documentation
- an anonymized public release at approximately 1% of paper scale
- benchmark submission schemas
- public-release benchmark assets for Task A and Task B
- slim public reproducibility scripts for release validation and paper-facing checks
- release manifests, checksums, anonymization notes, and flag definitions
- release-facing benchmark reference files

This stage is large enough to be benchmark-relevant, while still respecting release constraints. The public tables keep paper-faithful schema semantics, stable surrogate entity IDs, normalized public jurisdiction codes, and deterministic ambiguity flags, while omitting source-side names and mapping surfaces.

## Stage 2: planned as an expanded post-publication release

Subject to source-distribution and compliance constraints, a later expanded release may add:

- larger or full schema-stable data tables
- official full benchmark instance lists and candidate sets
- expanded reference artifacts for Task A and Task B
- richer per-year snapshot materials
- fuller provenance hooks and versioned maintenance metadata

## What may remain restricted even after publication

Depending on source permissions and compliance review, the public release may still omit or downscope:

- source-native identifiers
- direct source-to-release mapping tables
- raw source registry strings
- provenance fields that expose non-redistributable internals
- benchmark artifacts that directly leak protected source structure

## Canonical release wording

Use wording that is accurate and consistent across the paper, appendix, release page, and repository:

> We release an anonymized public artifact containing schema documentation, release-scale data tables, benchmark interfaces, public reference files, release validation scripts, and release documentation. Expanded releases remain subject to source-distribution and compliance constraints following publication.

## What the repository supports today

The current repository is sufficient to:

- inspect the release schema and anonymization policy
- load and validate the anonymized public release tables
- rerun release-facing validation and public statistics scripts
- verify release integrity via manifest and checksums
- inspect the public benchmark interface and released references

The repository does **not** claim that the full production-scale benchmark bundle is already public.
