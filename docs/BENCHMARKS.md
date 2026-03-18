# Benchmark Interface

The public repository exposes a **paper-aligned benchmark surface** centered on the `public_release` assets for the anonymized 1%-scale release.

The repository still does **not** claim that the full production benchmark population is already public.

## Task A: target-level tracing with evidence paths

**Input**: `(year, target, candidate_set)`

**Output**:

- `prediction`
- `ranked_predictions`
- `evidence_paths`

**Public evaluator checks**:

- `Top-1`
- `Top-5`
- `ValidPath`
- `InstValid`
- `AuditCov`
- compactness summaries

## Task B: capital-group extraction with witness subgraphs

**Input**: a yearly snapshot universe

**Output**:

- predicted groups
- witness subgraphs

**Public evaluator checks**:

- `ARI`
- `Pair-F1`
- `ValidSubg`
- `MemberCov`
- witness-size summaries

## Public artifact tier

### Public release tier

Files under `benchmarks/public_release/` contain:

- train / val / test instance lists
- public reference outputs
- Task A instance files with `instance_id` and `candidate_set`
- Task A reference files with ranked predictions and up to `P=5` evidence paths
- Task B instance files whose `universe` encodes the year-specific evaluation universe with near-boundary negatives
- Task B reference files with one or more groups plus compact witness subgraphs

Released benchmark scale:

- Task A targets: `16,200 / 4,800 / 5,200` for train / val / test
- Task B groups: `784 / 269 / 287` for train / val / test

In this public tier, Task B instance-file row counts are smaller than Task B group totals because each released instance can contain multiple reference groups inside one yearly evaluation universe.

## What is not claimed today

The public repository does not claim to expose:

- the full benchmark instance population
- the complete candidate sets used in the paper-scale release
- full reference bundles for all paper experiments
- a public leaderboard over the non-public benchmark tier

That material is reserved for an expanded release subject to post-publication compliance review.
