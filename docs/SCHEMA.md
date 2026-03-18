# Release Schema

## Core tables

### `entities`

| field | type | description |
|---|---|---|
| `entity_id` | string | stable release identifier |
| `entity_type` | string | company / branch / partnership / institutional_investor / ... |
| `jurisdiction_code` | string | normalized public jurisdiction code |
| `country_code` | string | ISO-style country code when available |
| `status` | string | normalized entity status |
| `flags` | string | pipe-separated quality or ambiguity flags |

### `ownership_edges`

| field | type | description |
|---|---|---|
| `src` | string | shareholder entity ID |
| `dst` | string | investee entity ID |
| `w` | float | normalized stake in `[0, 1]` |
| `t_start` | string | start date, typically `YYYY-MM-DD` |
| `t_end` | string | end date, empty when open-ended |
| `prov` | string | release-level provenance channel |
| `flags` | string | pipe-separated temporal / quality flags |

`ownership_edges` is the **only** table used to assert shareholding semantics and time-valid penetration evidence.

### `aux_relations`

| field | type | description |
|---|---|---|
| `rel_id` | string | stable relation ID |
| `src` | string | source node |
| `dst` | string | destination node |
| `rel_type` | string | executive-role / organizational-link / ... |
| `t_start` | string | start date if available |
| `t_end` | string | end date if available |
| `prov` | string | release-level provenance channel |
| `flags` | string | pipe-separated ambiguity flags |

### `metadata`

The public release uses manifest-style metadata under `metadata/` rather than a standalone metadata CSV table. Public-release metadata includes anonymization notes, redaction guidance, the release manifest, checksums, summary counts, and release-facing validation assets under `scripts/`.

## Temporal semantics

An ownership edge is active in calendar year `y` iff:

`start <= 31-Dec-y and (end is empty or end >= 01-Jan-y)`

## Consolidation and flags

The paper's release policy is reflected in the public release:
- repeated filings are consolidated deterministically where possible
- overlapping intervals are not unioned silently
- ambiguity is surfaced through flags rather than erased

See `metadata/flag_dictionary.csv` for release-level flag definitions.
