# FinCorpNet Data Card

## 1. Summary

FinCorpNet is a temporal corporate ownership graph for research on **equity penetration analysis** under explicit snapshot semantics. The public repository releases an **anonymized 1%-scale artifact** derived from the same China-centered registry, shareholding-filing, and auxiliary-record construction logic described in the KDD 2026 paper, packaged as a release-safe public subset rather than the full production corpus.

Released public counts:

- `584,000` entities
- `3,227,000` temporal ownership-edge records
- `1,561,000` auxiliary relation records
- coverage over `1990-2025`

The public artifact preserves the same logical data model and benchmark boundary as the full release described in the paper, while replacing source-native identifiers with stable surrogate IDs and publishing normalized public jurisdiction codes. Public entity names are omitted from the released tables, and the released slice is curated to retain heterogeneous ownership motifs, cross-holdings, year-to-year churn, and auxiliary context without disclosing source-native strings.

## 2. Released artifacts

The release centers four artifact families:

- `entities`
- `ownership_edges`
- `aux_relations`
- `metadata`

Among these, `ownership_edges` is the **authoritative source** for shareholding semantics and time-valid evidence.

## 3. Intended use

The public release is intended for:

- temporal graph mining research
- auditable controller-style tracing
- capital-group extraction with witness validation
- benchmark onboarding for Task A and Task B
- reproducibility checks for the public release workflow
- reviewer-facing artifact verification

## 4. Out-of-scope use

This resource should not be used as the sole basis for:

- legal or regulatory determinations
- beneficial-ownership claims without human review
- sanctions, enforcement, or adverse decisions
- direct redistribution of source-native content beyond the documented release scope

## 5. Source families and anonymization

The full benchmark integrates three record families:

1. legal-entity registry records
2. shareholding and filing records with stake information
3. executive and organizational links released as complementary context

The public release is distributed in anonymized form:

- entity identifiers are replaced with stable public surrogate IDs
- public entity names are omitted from the released tables
- provenance is collapsed to source-family level channels while preserving temporal anchoring semantics
- jurisdiction codes are normalized to a public release code space centered on PRC province-level codes, with limited offshore or special-region codes retained when needed for the anonymized public export
- release-safe flags are retained for downstream filtering and auditability

See [`metadata/anonymization_policy.md`](metadata/anonymization_policy.md) and [`metadata/redaction_dictionary.csv`](metadata/redaction_dictionary.csv).

## 6. Data model and temporal semantics

Each ownership edge is represented as:

`(src, dst, w, t_start, t_end, prov, flags)`

where:

- `src` is the shareholder entity ID
- `dst` is the investee entity ID
- `w` is the normalized stake in `[0, 1]`
- `t_start` and `t_end` define the validity interval
- `prov` identifies the release-level provenance channel
- `flags` preserves ambiguity and data-quality signals

An edge is active in year `y` iff its validity interval intersects the calendar year. All benchmark evidence in this public repository is checked against that rule.

## 7. Quality controls

The published release bundle is checked for:

- endpoint existence
- weight parsing and range constraints
- interval consistency
- release-year envelope consistency (`1990-2025`)
- snapshot-valid evidence checking in the public benchmark scripts
- ambiguity surfacing via flags rather than hidden imputation
- manifest and checksum verification of released artifacts
- public-script reproducibility of release-facing validation and summary checks

## 8. Flags and ambiguity policy

The release keeps flagged records visible so downstream users can make their own filtering decisions. Example flags include:

- `open_ended`
- `date_from_filing`
- `t_end_known`
- `t_end_unknown`
- `stake_change`
- `overlap_interval`
- `conflicting_events`
- `cyclic_scc`
- `minority_link`
- `weak_path`
- `id_conflict`
- `weak_match`

See [`metadata/flag_dictionary.csv`](metadata/flag_dictionary.csv) for release-level definitions.

## 9. Public release subset

The released tables under [`data-public/`](data-public/) are not the full production-scale artifact from the paper. They represent an approximately **1% anonymized public release tier** designed to preserve:

- multi-hop ownership chains
- strongly connected components / cross-holdings
- open-ended validity intervals
- year-to-year changes in active edge sets
- auxiliary non-ownership context
- benchmark-compatible controller and group examples

The public subset is constructed to retain mixed local structures rather than a single repeated component template, so users should expect variation in local graph size, path depth, minority stakes, and effective date patterns across released regions.

The upload bundle intentionally excludes development-only extras and focuses on the release-scale public artifacts.

## 10. Benchmark tasks

### Task A: Target-level tracing with evidence paths

Input: `(year, target, candidate_set)`

Expected output:

- a predicted controller-style node
- a ranked candidate list
- one or more snapshot-valid evidence paths

### Task B: Group extraction with witness subgraphs

Input: a yearly snapshot universe

Expected output:

- predicted groups
- a witness edge set per group
- evidence that supports member inclusion under the same snapshot semantics

## 11. Risks and limitations

- controller-style labels are benchmark proxies, not legal truth
- temporal fields may inherit source-side incompleteness
- auxiliary links are contextual only and do not assert ownership evidence
- the public release is anonymized and therefore not intended for source-level provenance tracing
- the public artifact is only about 1% of the full paper-scale resource
- the full production-scale benchmark is not yet redistributed here

## 12. Release status

This repository is the **public anonymized release tier**. The roadmap remains:

- now: 1%-scale anonymized release, public benchmark tier, release validation scripts, manifests, and release documentation
- later: larger or full data tables and expanded benchmark artifact bundles, subject to post-publication review

See [`RELEASE_POLICY.md`](RELEASE_POLICY.md) and [`docs/ARTIFACT_AVAILABILITY.md`](docs/ARTIFACT_AVAILABILITY.md) for the exact release boundary.
