import csv
import json
import re
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASELINE_DIR = PROJECT_ROOT / "data" / "revised"
CLAUDE_DIR = PROJECT_ROOT / "data" / "claude"
OUT_DIR = PROJECT_ROOT / "outputs" / "comparison"
ROUNDTRIP_DIR = PROJECT_ROOT / "outputs" / "roundtrip"

DATASETS = [
    ("User", BASELINE_DIR / "user_dataset.csv", CLAUDE_DIR / "claude_user_dataset.csv"),
    ("Food Ministry", BASELINE_DIR / "food_ministry_dataset.csv", CLAUDE_DIR / "claude_food_ministry_dataset.csv"),
    ("Food Industry", BASELINE_DIR / "food_industry_dataset.csv", CLAUDE_DIR / "claude_food_industry_dataset.csv"),
]

FORMULA_COLUMNS = ["implication_formula", "dyadic_formula"]
PREDICATE_RE = re.compile(r"([A-Za-z][A-Za-z0-9_]*)\(")


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def predicates(rows):
    found = Counter()
    for row in rows:
        for column in FORMULA_COLUMNS:
            for name in PREDICATE_RE.findall(row[column]):
                if name not in {"O", "P", "F"}:
                    found[name] += 1
    return found


def condition_size(formula):
    if "->" in formula:
        condition = formula.split("->", 1)[0]
        condition = condition.replace("∀x.∀y.", "")
    elif "|" in formula:
        condition = formula.rsplit("|", 1)[1].rstrip(")")
    else:
        return 0
    parts = re.split(r"[∧∨]", condition)
    return len([p for p in parts if p.strip()])


def norm_counts(rows):
    return Counter(row["norm_type"] for row in rows)


def duplicate_count(rows, field):
    values = [row[field] for row in rows]
    return len(values) - len(set(values))


def exact_overlap(left_rows, right_rows, field):
    left = {row[field] for row in left_rows}
    right = {row[field] for row in right_rows}
    return len(left & right), len(left), len(right)


def compare_by_id(left_rows, right_rows):
    left_by_id = {row["id"]: row for row in left_rows}
    right_by_id = {row["id"]: row for row in right_rows}
    shared_ids = sorted(set(left_by_id) & set(right_by_id))
    same_norm_type = 0
    same_implication = 0
    same_dyadic = 0
    same_nl = 0
    examples = []

    for row_id in shared_ids:
        left = left_by_id[row_id]
        right = right_by_id[row_id]
        same_norm_type += left["norm_type"] == right["norm_type"]
        same_implication += left["implication_formula"] == right["implication_formula"]
        same_dyadic += left["dyadic_formula"] == right["dyadic_formula"]
        same_nl += left["nl_norm"] == right["nl_norm"]
        if len(examples) < 5 and left["implication_formula"] != right["implication_formula"]:
            examples.append({
                "id": row_id,
                "baseline_nl": left["nl_norm"],
                "claude_nl": right["nl_norm"],
                "baseline_implication": left["implication_formula"],
                "claude_implication": right["implication_formula"],
            })

    return {
        "shared_ids": len(shared_ids),
        "same_norm_type": same_norm_type,
        "same_nl": same_nl,
        "same_implication_formula": same_implication,
        "same_dyadic_formula": same_dyadic,
        "different_formula_examples": examples,
    }


def summarize_dataset(stakeholder, baseline_path, claude_path):
    baseline = read_csv(baseline_path)
    claude = read_csv(claude_path)
    baseline_preds = predicates(baseline)
    claude_preds = predicates(claude)
    shared_predicates = set(baseline_preds) & set(claude_preds)

    summary = {
        "stakeholder": stakeholder,
        "baseline_rows": len(baseline),
        "claude_rows": len(claude),
        "baseline_formulas": len(baseline) * 2,
        "claude_formulas": len(claude) * 2,
        "baseline_norm_types": dict(norm_counts(baseline)),
        "claude_norm_types": dict(norm_counts(claude)),
        "baseline_duplicate_nl": duplicate_count(baseline, "nl_norm"),
        "claude_duplicate_nl": duplicate_count(claude, "nl_norm"),
        "baseline_predicate_count": len(baseline_preds),
        "claude_predicate_count": len(claude_preds),
        "shared_predicate_count": len(shared_predicates),
        "baseline_only_predicates": sorted(set(baseline_preds) - set(claude_preds))[:30],
        "claude_only_predicates": sorted(set(claude_preds) - set(baseline_preds))[:30],
        "avg_baseline_condition_size": round(sum(condition_size(row["implication_formula"]) for row in baseline) / len(baseline), 2),
        "avg_claude_condition_size": round(sum(condition_size(row["implication_formula"]) for row in claude) / len(claude), 2),
        "by_id": compare_by_id(baseline, claude),
    }

    for field in ["nl_norm", "implication_formula", "dyadic_formula"]:
        count, baseline_total, claude_total = exact_overlap(baseline, claude, field)
        summary[f"exact_{field}_overlap"] = count
        summary[f"exact_{field}_overlap_percent_of_claude"] = round(100 * count / claude_total, 1) if claude_total else 0

    return summary


def md_counter(counter_dict):
    if not counter_dict:
        return "-"
    return ", ".join(f"{key}: {value}" for key, value in sorted(counter_dict.items()))


def write_markdown(summaries):
    baseline_scores = roundtrip_score_counts(ROUNDTRIP_DIR / "roundtrip_evaluated.csv")
    claude_scores = roundtrip_score_counts(ROUNDTRIP_DIR / "claude_roundtrip_evaluated.csv")
    lines = [
        "# Claude vs Baseline Dataset Comparison",
        "",
        "Claude metadata supplied by Viktor:",
        "",
        "- LLM: Claude",
        "- Model/version: Claude Opus 4.8, High effort",
        "- Date generated: 2026-06-28",
        "- Prompt file used: GitHub stakeholder prompt files",
        "- Fresh chat: yes",
        "- Manual edits: none",
        "",
        "## Validation Result",
        "",
        "The three Claude stakeholder datasets were validated using the same `scripts/validate_revised_datasets.py` parser validation used for the baseline revised datasets.",
        "",
        "| Source | Records | Formulas | Errors | Warnings |",
        "|---|---:|---:|---:|---:|",
        "| Baseline revised stakeholder datasets | 300 | 600 | 0 | 0 |",
        "| Claude stakeholder datasets | 300 | 600 | 0 | 0 |",
        "",
        "Note: Claude constitutive rules were not provided in this batch, so this comparison covers the three stakeholder datasets only.",
        "",
        "## Round-Trip Automatic Evaluation",
        "",
        "| Source | Rows | Score 2 | Score 1 | Score 0 |",
        "|---|---:|---:|---:|---:|",
        f"| Baseline revised stakeholder datasets | {sum(baseline_scores.values())} | {baseline_scores.get('2', 0)} | {baseline_scores.get('1', 0)} | {baseline_scores.get('0', 0)} |",
        f"| Claude stakeholder datasets | {sum(claude_scores.values())} | {claude_scores.get('2', 0)} | {claude_scores.get('1', 0)} | {claude_scores.get('0', 0)} |",
        "",
        "These automatic scores are heuristic triage results. Human review is still required for semantic accuracy.",
        "",
        "## Summary by Stakeholder",
        "",
        "| Stakeholder | Claude rows | Claude formulas | Exact NL overlap | Exact implication overlap | Exact dyadic overlap | Shared predicates | Avg condition size baseline | Avg condition size Claude |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for item in summaries:
        lines.append(
            f"| {item['stakeholder']} | {item['claude_rows']} | {item['claude_formulas']} | "
            f"{item['exact_nl_norm_overlap']} | {item['exact_implication_formula_overlap']} | "
            f"{item['exact_dyadic_formula_overlap']} | {item['shared_predicate_count']} | "
            f"{item['avg_baseline_condition_size']} | {item['avg_claude_condition_size']} |"
        )

    lines.extend(["", "## Norm-Type Distribution", ""])
    for item in summaries:
        lines.extend([
            f"### {item['stakeholder']}",
            "",
            f"- Baseline: {md_counter(item['baseline_norm_types'])}",
            f"- Claude: {md_counter(item['claude_norm_types'])}",
            "",
        ])

    lines.extend(["## Predicate Vocabulary Differences", ""])
    for item in summaries:
        lines.extend([
            f"### {item['stakeholder']}",
            "",
            f"- Baseline predicate count: {item['baseline_predicate_count']}",
            f"- Claude predicate count: {item['claude_predicate_count']}",
            f"- Shared predicates: {item['shared_predicate_count']}",
            f"- Baseline-only examples: {', '.join(item['baseline_only_predicates']) or '-'}",
            f"- Claude-only examples: {', '.join(item['claude_only_predicates']) or '-'}",
            "",
        ])

    lines.extend([
        "## Initial Interpretation",
        "",
        "Both datasets pass syntactic validation under the fixed grammar. This means Claude was able to follow the grammar and revised formula conventions for the three stakeholder datasets.",
        "",
        "The more important comparison is now semantic and design-oriented: whether Claude's norms are as stakeholder-specific, diverse, and useful for conflict detection as the baseline dataset. Exact formula overlap is expected to be limited because Claude generated new records from the same prompt rather than reproducing the baseline rows exactly.",
        "",
        "Recommended next step: perform human semantic review on a sample of baseline and Claude round-trip rows, especially rows with automatic scores 0 or 1, and then compare whether the smaller Claude predicate vocabulary affects conflict-detection usefulness.",
    ])

    (OUT_DIR / "claude_vs_baseline_comparison.md").write_text("\n".join(lines), encoding="utf-8")


def write_csv_summary(summaries):
    fieldnames = [
        "stakeholder",
        "baseline_rows",
        "claude_rows",
        "baseline_formulas",
        "claude_formulas",
        "exact_nl_norm_overlap",
        "exact_implication_formula_overlap",
        "exact_dyadic_formula_overlap",
        "baseline_predicate_count",
        "claude_predicate_count",
        "shared_predicate_count",
        "avg_baseline_condition_size",
        "avg_claude_condition_size",
    ]
    with (OUT_DIR / "claude_vs_baseline_summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in summaries:
            writer.writerow({field: item[field] for field in fieldnames})


def roundtrip_score_counts(path):
    if not path.exists():
        return Counter()
    with path.open(encoding="utf-8", newline="") as f:
        return Counter(row["auto_semantic_score"] for row in csv.DictReader(f))


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summaries = [summarize_dataset(*dataset) for dataset in DATASETS]
    (OUT_DIR / "claude_vs_baseline_comparison.json").write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_markdown(summaries)
    write_csv_summary(summaries)
    print(f"Wrote comparison outputs to {OUT_DIR}")


if __name__ == "__main__":
    main()
