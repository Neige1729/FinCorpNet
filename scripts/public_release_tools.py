from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from datetime import date
from itertools import combinations
from pathlib import Path
from statistics import median
from typing import Iterable


TASK_A_REQUIRED_FIELDS = {"instance_id", "year", "target", "prediction", "ranked_predictions", "evidence_paths"}
TASK_B_REQUIRED_FIELDS = {"instance_id", "year", "groups"}
TASK_B_GROUP_REQUIRED_FIELDS = {"controller", "members", "witness_edges"}
MIN_YEAR = 1990
MAX_YEAR = 2025


@dataclass(frozen=True)
class BenchmarkConfig:
    min_weight: float = 0.25
    max_path_length: int = 12
    max_paths: int = 5
    witness_budget: int = 200


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_csv_rows(path: str | Path) -> Iterable[dict[str, str]]:
    with Path(path).open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            yield row


def read_jsonl(path: str | Path) -> list[dict]:
    rows: list[dict] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at line {line_no} in {path}: {exc}") from exc
    return rows


def parse_date(value: str) -> date:
    value = value.strip()
    if not value:
        raise ValueError("empty date")
    if len(value) == 4 and value.isdigit():
        return date(int(value), 1, 1)
    return date.fromisoformat(value)


def parse_weight(value: str | float) -> float:
    return float(value)


def intersects_year(t_start: str, t_end: str, year: int) -> bool:
    start = parse_date(t_start)
    end = date.max if not t_end.strip() else parse_date(t_end)
    return start <= date(year, 12, 31) and end >= date(year, 1, 1)


def active_edge_map(rows: Iterable[dict[str, str]], year: int) -> dict[tuple[str, str], dict[str, str]]:
    best: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        if not intersects_year(row["t_start"], row.get("t_end", ""), year):
            continue
        key = (row["src"], row["dst"])
        current = best.get(key)
        if current is None or parse_weight(row["w"]) > parse_weight(current["w"]):
            best[key] = row
    return best


def build_adjacency(rows: Iterable[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    adjacency: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        adjacency[row["src"]].append(row)
    for values in adjacency.values():
        values.sort(key=lambda row: (row["dst"], -parse_weight(row["w"])))
    return dict(adjacency)


def path_is_simple(path: list[str]) -> bool:
    return len(path) >= 2 and len(path) == len(set(path))


def path_is_valid(
    path: list[str],
    edge_map: dict[tuple[str, str], dict[str, str]],
    min_weight: float = 0.25,
    max_length: int = 12,
) -> bool:
    if not path_is_simple(path):
        return False
    if len(path) - 1 > max_length:
        return False
    for src, dst in zip(path[:-1], path[1:]):
        row = edge_map.get((src, dst))
        if row is None or parse_weight(row["w"]) < min_weight:
            return False
    return True


def _comb2(value: int) -> float:
    return value * (value - 1) / 2.0


def adjusted_rand_index(labels_true: list[str], labels_pred: list[str]) -> float:
    if len(labels_true) != len(labels_pred):
        raise ValueError("Label vectors must have the same length")
    total = len(labels_true)
    if total <= 1:
        return 1.0
    contingency: dict[tuple[str, str], int] = Counter(zip(labels_true, labels_pred))
    true_counts = Counter(labels_true)
    pred_counts = Counter(labels_pred)
    sum_index = sum(_comb2(value) for value in contingency.values())
    sum_true = sum(_comb2(value) for value in true_counts.values())
    sum_pred = sum(_comb2(value) for value in pred_counts.values())
    total_pairs = _comb2(total)
    expected = (sum_true * sum_pred) / total_pairs if total_pairs else 0.0
    max_index = 0.5 * (sum_true + sum_pred)
    denom = max_index - expected
    if denom == 0:
        return 1.0 if labels_true == labels_pred else 0.0
    return (sum_index - expected) / denom


def pair_f1(labels_true: list[str], labels_pred: list[str]) -> float:
    if len(labels_true) != len(labels_pred):
        raise ValueError("Label vectors must have the same length")
    if len(labels_true) <= 1:
        return 1.0
    true_pairs = {
        (i, j) for i, j in combinations(range(len(labels_true)), 2) if labels_true[i] == labels_true[j]
    }
    pred_pairs = {
        (i, j) for i, j in combinations(range(len(labels_pred)), 2) if labels_pred[i] == labels_pred[j]
    }
    if not true_pairs and not pred_pairs:
        return 1.0
    tp = len(true_pairs & pred_pairs)
    precision = tp / len(pred_pairs) if pred_pairs else 0.0
    recall = tp / len(true_pairs) if true_pairs else 0.0
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def validate_release(manifest_path: str | Path, checksums_path: str | Path) -> dict[str, object]:
    manifest_path = Path(manifest_path)
    base = manifest_path.parent.parent
    missing: list[str] = []
    manifest_rows = 0
    with manifest_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            manifest_rows += 1
            if not (base / row["path"]).exists():
                missing.append(row["path"])
    checksum_errors: list[str] = []
    with Path(checksums_path).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            digest, rel = line.split("  ", 1)
            target = base / rel
            if not target.exists() or sha256_file(target) != digest:
                checksum_errors.append(rel)
    entity_ids = {row["entity_id"] for row in iter_csv_rows(base / "data-public" / "entities" / "entities_public_1pct.csv")}
    ownership_errors = {
        "endpoint_missing": 0,
        "weight_out_of_range": 0,
        "date_parse_error": 0,
        "interval_inconsistent": 0,
        "year_out_of_range": 0,
    }
    aux_errors = {
        "endpoint_missing": 0,
        "date_parse_error": 0,
        "interval_inconsistent": 0,
        "year_out_of_range": 0,
    }
    ownership_examples: list[str] = []
    aux_examples: list[str] = []

    def _track_example(bucket: list[str], text: str) -> None:
        if len(bucket) < 5:
            bucket.append(text)

    for row_idx, row in enumerate(iter_csv_rows(base / "data-public" / "ownership_edges" / "ownership_edges_public_1pct.csv"), start=2):
        if row["src"] not in entity_ids or row["dst"] not in entity_ids:
            ownership_errors["endpoint_missing"] += 1
            _track_example(ownership_examples, f"ownership row {row_idx}: missing endpoint")
        try:
            weight = parse_weight(row["w"])
            if not (0.0 < weight <= 1.0):
                ownership_errors["weight_out_of_range"] += 1
                _track_example(ownership_examples, f"ownership row {row_idx}: weight {row['w']}")
        except Exception:
            ownership_errors["weight_out_of_range"] += 1
            _track_example(ownership_examples, f"ownership row {row_idx}: invalid weight {row['w']}")
        try:
            start = parse_date(row["t_start"])
            end = parse_date(row["t_end"]) if row.get("t_end", "").strip() else None
        except Exception:
            ownership_errors["date_parse_error"] += 1
            _track_example(ownership_examples, f"ownership row {row_idx}: invalid date")
            continue
        if not (MIN_YEAR <= start.year <= MAX_YEAR) or (end is not None and not (MIN_YEAR <= end.year <= MAX_YEAR)):
            ownership_errors["year_out_of_range"] += 1
            _track_example(ownership_examples, f"ownership row {row_idx}: year out of range")
        if end is not None and start > end:
            ownership_errors["interval_inconsistent"] += 1
            _track_example(ownership_examples, f"ownership row {row_idx}: start {start.isoformat()} > end {end.isoformat()}")

    for row_idx, row in enumerate(iter_csv_rows(base / "data-public" / "aux_relations" / "aux_relations_public_1pct.csv"), start=2):
        if row["src"] not in entity_ids or row["dst"] not in entity_ids:
            aux_errors["endpoint_missing"] += 1
            _track_example(aux_examples, f"aux row {row_idx}: missing endpoint")
        try:
            start = parse_date(row["t_start"])
            end = parse_date(row["t_end"]) if row.get("t_end", "").strip() else None
        except Exception:
            aux_errors["date_parse_error"] += 1
            _track_example(aux_examples, f"aux row {row_idx}: invalid date")
            continue
        if not (MIN_YEAR <= start.year <= MAX_YEAR) or (end is not None and not (MIN_YEAR <= end.year <= MAX_YEAR)):
            aux_errors["year_out_of_range"] += 1
            _track_example(aux_examples, f"aux row {row_idx}: year out of range")
        if end is not None and start > end:
            aux_errors["interval_inconsistent"] += 1
            _track_example(aux_examples, f"aux row {row_idx}: start {start.isoformat()} > end {end.isoformat()}")
    return {
        "entries": manifest_rows,
        "missing": missing,
        "checksum_errors": checksum_errors,
        "ownership_errors": ownership_errors,
        "ownership_examples": ownership_examples,
        "aux_errors": aux_errors,
        "aux_examples": aux_examples,
    }


def _instance_ids(items: list[dict]) -> set[str]:
    ids = []
    for item in items:
        instance_id = item.get("instance_id")
        if not isinstance(instance_id, str) or not instance_id:
            raise ValueError("Every benchmark row must include a non-empty instance_id")
        ids.append(instance_id)
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate instance_id values found")
    return set(ids)


def validate_task_a_submission(submission: list[dict], instances: list[dict]) -> dict[str, object]:
    errors: list[str] = []
    valid_ids = _instance_ids(instances)
    seen_ids: set[str] = set()
    for idx, item in enumerate(submission):
        missing = TASK_A_REQUIRED_FIELDS - set(item)
        if missing:
            errors.append(f"row {idx}: missing fields {sorted(missing)}")
            continue
        if item["instance_id"] in seen_ids:
            errors.append(f"row {idx}: duplicate instance_id {item['instance_id']}")
        seen_ids.add(item["instance_id"])
        if item["instance_id"] not in valid_ids:
            errors.append(f"row {idx}: unknown instance_id {item['instance_id']}")
        if not isinstance(item["ranked_predictions"], list) or not item["ranked_predictions"]:
            errors.append(f"row {idx}: ranked_predictions must be a non-empty list")
        if item["prediction"] not in item.get("ranked_predictions", []):
            errors.append(f"row {idx}: prediction must appear in ranked_predictions")
        if len(item.get("ranked_predictions", [])) > 5:
            errors.append(f"row {idx}: ranked_predictions exceeds public Top-5 limit")
        if not isinstance(item.get("evidence_paths"), list):
            errors.append(f"row {idx}: evidence_paths must be a list")
            continue
        if len(item["evidence_paths"]) > 5:
            errors.append(f"row {idx}: evidence_paths exceeds public path limit")
    return {"ok": not errors, "errors": errors}


def validate_task_b_submission(submission: list[dict], instances: list[dict]) -> dict[str, object]:
    errors: list[str] = []
    valid_ids = _instance_ids(instances)
    seen_ids: set[str] = set()
    for idx, item in enumerate(submission):
        missing = TASK_B_REQUIRED_FIELDS - set(item)
        if missing:
            errors.append(f"row {idx}: missing fields {sorted(missing)}")
            continue
        if item["instance_id"] in seen_ids:
            errors.append(f"row {idx}: duplicate instance_id {item['instance_id']}")
        seen_ids.add(item["instance_id"])
        if item["instance_id"] not in valid_ids:
            errors.append(f"row {idx}: unknown instance_id {item['instance_id']}")
        groups = item.get("groups")
        if not isinstance(groups, list):
            errors.append(f"row {idx}: groups must be a list")
            continue
        assigned: set[str] = set()
        for group_idx, group in enumerate(groups):
            missing_group = TASK_B_GROUP_REQUIRED_FIELDS - set(group)
            if missing_group:
                errors.append(f"row {idx}: group {group_idx} missing {sorted(missing_group)}")
                continue
            overlap = assigned & set(group.get("members", []))
            if overlap:
                errors.append(f"row {idx}: overlapping members across groups {sorted(overlap)}")
            assigned |= set(group.get("members", []))
    return {"ok": not errors, "errors": errors}


def _labels_from_groups(universe: list[str], groups: list[dict]) -> list[str]:
    labels: dict[str, str] = {}
    for group in groups:
        controller = group["controller"]
        for member in group.get("members", []):
            labels.setdefault(member, controller)
    return [labels.get(node, f"singleton:{node}") for node in universe]


def _witness_paths_exist(
    controller: str,
    member: str,
    witness_edges: list[list[str]],
    edge_map: dict[tuple[str, str], dict[str, str]],
    config: BenchmarkConfig,
) -> bool:
    sub_rows = []
    for edge in witness_edges:
        if len(edge) != 2:
            continue
        row = edge_map.get((edge[0], edge[1]))
        if row is not None:
            sub_rows.append(row)
    adjacency = build_adjacency(sub_rows)
    stack: list[tuple[str, list[str]]] = [(controller, [controller])]
    while stack:
        node, path = stack.pop()
        if len(path) - 1 > config.max_path_length:
            continue
        if node == member and path_is_valid(path, edge_map, config.min_weight, config.max_path_length):
            return True
        for row in adjacency.get(node, []):
            nxt = row["dst"]
            if nxt in path:
                continue
            stack.append((nxt, path + [nxt]))
    return False


def evaluate_task_a(
    submission: list[dict],
    references: list[dict],
    active_edges: Iterable[dict[str, str]],
    config: BenchmarkConfig | None = None,
) -> dict[str, float | int]:
    config = config or BenchmarkConfig()
    rows = list(active_edges)
    year_maps: dict[int, dict[tuple[str, str], dict[str, str]]] = {}
    ref_map = {row["instance_id"]: row for row in references}
    total = top1 = top5 = valid_path_count = returned_path_count = inst_valid = audit_cov = 0
    shortest_valid_lengths: list[int] = []
    used_edge_counts: list[int] = []
    for item in submission:
        ref = ref_map.get(item["instance_id"])
        if ref is None:
            continue
        year = int(ref["year"])
        edge_map = year_maps.setdefault(year, active_edge_map(rows, year))
        total += 1
        if item["prediction"] == ref["prediction"]:
            top1 += 1
        if ref["prediction"] in item.get("ranked_predictions", [])[:5]:
            top5 += 1
        valid_paths = [
            path for path in item.get("evidence_paths", []) if path_is_valid(path, edge_map, config.min_weight, config.max_path_length)
        ]
        valid_path_count += len(valid_paths)
        returned_path_count += len(item.get("evidence_paths", []))
        if valid_paths:
            inst_valid += 1
            shortest_valid_lengths.append(min(len(path) - 1 for path in valid_paths))
            used_edge_counts.append(len({(src, dst) for path in valid_paths for src, dst in zip(path[:-1], path[1:])}))
        if item["prediction"] == ref["prediction"] and valid_paths:
            audit_cov += 1
    return {
        "total": total,
        "top1_rate": round(top1 / total, 6) if total else 0.0,
        "top5_rate": round(top5 / total, 6) if total else 0.0,
        "valid_path_rate": round(valid_path_count / returned_path_count, 6) if returned_path_count else 0.0,
        "inst_valid_rate": round(inst_valid / total, 6) if total else 0.0,
        "audit_cov_rate": round(audit_cov / total, 6) if total else 0.0,
        "avg_shortest_valid_path_len": round(sum(shortest_valid_lengths) / len(shortest_valid_lengths), 6) if shortest_valid_lengths else 0.0,
        "median_distinct_evidence_edges": float(median(used_edge_counts)) if used_edge_counts else 0.0,
    }


def evaluate_task_b(
    submission: list[dict],
    references: list[dict],
    active_edges: Iterable[dict[str, str]],
    config: BenchmarkConfig | None = None,
) -> dict[str, float | int]:
    config = config or BenchmarkConfig()
    rows = list(active_edges)
    year_maps: dict[int, dict[tuple[str, str], dict[str, str]]] = {}
    ref_map = {row["instance_id"]: row for row in references}
    total = valid_subg = 0
    ari_scores: list[float] = []
    pair_scores: list[float] = []
    member_cov_scores: list[float] = []
    witness_sizes: list[int] = []
    for item in submission:
        ref = ref_map.get(item["instance_id"])
        if ref is None:
            continue
        year = int(ref["year"])
        edge_map = year_maps.setdefault(year, active_edge_map(rows, year))
        total += 1
        pred_groups = item.get("groups", [])
        ref_groups = ref.get("groups", [])
        universe = sorted({member for group in ref_groups for member in group.get("members", [])} | set(ref.get("universe", [])))
        if universe:
            ari_scores.append(adjusted_rand_index(_labels_from_groups(universe, ref_groups), _labels_from_groups(universe, pred_groups)))
            pair_scores.append(pair_f1(_labels_from_groups(universe, ref_groups), _labels_from_groups(universe, pred_groups)))
        subgraph_ok = True
        supported = total_members = witness_total = 0
        for group in pred_groups:
            witness_edges = group.get("witness_edges", [])
            witness_total += len(witness_edges)
            for edge in witness_edges:
                if not isinstance(edge, list) or len(edge) != 2:
                    subgraph_ok = False
                    continue
                row = edge_map.get((edge[0], edge[1]))
                if row is None or parse_weight(row["w"]) < config.min_weight:
                    subgraph_ok = False
            for member in group.get("members", []):
                total_members += 1
                if _witness_paths_exist(group["controller"], member, witness_edges, edge_map, config):
                    supported += 1
        if subgraph_ok:
            valid_subg += 1
        member_cov_scores.append(supported / total_members if total_members else 0.0)
        witness_sizes.append(witness_total)
    return {
        "total": total,
        "ari": round(sum(ari_scores) / len(ari_scores), 6) if ari_scores else 0.0,
        "pair_f1": round(sum(pair_scores) / len(pair_scores), 6) if pair_scores else 0.0,
        "valid_subg_rate": round(valid_subg / total, 6) if total else 0.0,
        "member_cov": round(sum(member_cov_scores) / len(member_cov_scores), 6) if member_cov_scores else 0.0,
        "median_witness_size": float(median(witness_sizes)) if witness_sizes else 0.0,
    }


def compute_public_stats(
    entities_path: Path,
    ownership_path: Path,
    aux_path: Path,
    year: int,
) -> dict[str, object]:
    entities = list(iter_csv_rows(entities_path))
    ownership_rows = list(iter_csv_rows(ownership_path))
    aux_rows = list(iter_csv_rows(aux_path))
    active_map = active_edge_map(ownership_rows, year)
    active_rows = list(active_map.values())
    nodes = {row["src"] for row in active_rows} | {row["dst"] for row in active_rows}
    entity_type_counts = Counter(row["entity_type"] for row in entities)
    ownership_flag_counts = Counter(flag for row in ownership_rows for flag in row.get("flags", "").split("|") if flag)
    aux_type_counts = Counter(row["rel_type"] for row in aux_rows)
    return {
        "year": year,
        "entity_count": len(entities),
        "ownership_edge_count": len(ownership_rows),
        "aux_relation_count": len(aux_rows),
        "active_ownership_edge_count": len(active_rows),
        "active_node_count": len(nodes),
        "entity_type_counts": dict(sorted(entity_type_counts.items())),
        "ownership_flag_counts": dict(sorted(ownership_flag_counts.items())),
        "aux_type_counts": dict(sorted(aux_type_counts.items())),
    }


def default_paths() -> dict[str, Path]:
    base = repo_root()
    return {
        "manifest": base / "metadata" / "public_release_manifest.csv",
        "checksums": base / "metadata" / "checksums.sha256",
        "entities": base / "data-public" / "entities" / "entities_public_1pct.csv",
        "ownership": base / "data-public" / "ownership_edges" / "ownership_edges_public_1pct.csv",
        "aux": base / "data-public" / "aux_relations" / "aux_relations_public_1pct.csv",
    }


def add_common_benchmark_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--task", required=True, choices=["task_a", "task_b"])
    parser.add_argument("--submission", required=True)
    parser.add_argument("--instances", required=True)
    parser.add_argument("--references", required=True)
    parser.add_argument("--edges", required=True)
