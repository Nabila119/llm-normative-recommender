import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from lark import Lark


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "outputs" / "comparison"

DATASETS = {
    "baseline": {
        "stakeholder_files": [
            PROJECT_ROOT / "data" / "revised" / "user_dataset.csv",
            PROJECT_ROOT / "data" / "revised" / "food_ministry_dataset.csv",
            PROJECT_ROOT / "data" / "revised" / "food_industry_dataset.csv",
        ],
        "ast_files": [
            PROJECT_ROOT / "outputs" / "asts" / "revised_user_asts.json",
            PROJECT_ROOT / "outputs" / "asts" / "revised_food_ministry_asts.json",
            PROJECT_ROOT / "outputs" / "asts" / "revised_food_industry_asts.json",
        ],
        "roundtrip_file": PROJECT_ROOT / "outputs" / "roundtrip" / "roundtrip_evaluated.csv",
    },
    "claude": {
        "stakeholder_files": [
            PROJECT_ROOT / "data" / "claude" / "claude_user_dataset.csv",
            PROJECT_ROOT / "data" / "claude" / "claude_food_ministry_dataset.csv",
            PROJECT_ROOT / "data" / "claude" / "claude_food_industry_dataset.csv",
        ],
        "ast_files": [
            PROJECT_ROOT / "outputs" / "asts" / "claude_user_dataset_asts.json",
            PROJECT_ROOT / "outputs" / "asts" / "claude_food_ministry_dataset_asts.json",
            PROJECT_ROOT / "outputs" / "asts" / "claude_food_industry_dataset_asts.json",
        ],
        "roundtrip_file": PROJECT_ROOT / "outputs" / "roundtrip" / "claude_roundtrip_evaluated.csv",
    },
}

FORMULA_COLUMNS = {
    "implication": "implication_formula",
    "dyadic": "dyadic_formula",
}

PREDICATE_RE = re.compile(r"([A-Za-z][A-Za-z0-9_]*)\(")


def load_parser():
    grammar = (PROJECT_ROOT / "grammar" / "grammar.lark").read_text(encoding="utf-8")
    return Lark(grammar, start="formula", parser="lalr")


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def ast_node_count(node):
    if isinstance(node, dict):
        return 1 + sum(ast_node_count(value) for value in node.values())
    if isinstance(node, list):
        return sum(ast_node_count(value) for value in node)
    return 0


def ast_depth(node):
    if isinstance(node, dict):
        child_depths = [ast_depth(value) for value in node.values()]
        return 1 + (max(child_depths) if child_depths else 0)
    if isinstance(node, list):
        return max([ast_depth(value) for value in node] or [0])
    return 0


def ast_predicate_count(node):
    if isinstance(node, dict):
        count = 1 if node.get("type") == "predicate" else 0
        return count + sum(ast_predicate_count(value) for value in node.values())
    if isinstance(node, list):
        return sum(ast_predicate_count(value) for value in node)
    return 0


def formula_predicate_count(formula):
    return len([name for name in PREDICATE_RE.findall(formula) if name not in {"O", "P", "F"}])


def average(values):
    return round(sum(values) / len(values), 2) if values else 0


def load_ast_metrics(ast_files):
    metrics = {}
    for path in ast_files:
        for row in read_json(path):
            for formula_type in FORMULA_COLUMNS:
                ast = row[f"{formula_type}_ast"]
                metrics[(row["id"], formula_type)] = {
                    "ast_node_count": ast_node_count(ast),
                    "ast_depth": ast_depth(ast),
                    "ast_predicate_count": ast_predicate_count(ast),
                }
    return metrics


def load_roundtrip(roundtrip_file):
    scores = {}
    for row in read_csv(roundtrip_file):
        scores[(row["id"], row["formula_type"])] = {
            "auto_semantic_score": row["auto_semantic_score"],
            "auto_error_type": row["auto_error_type"],
            "backtranslated_nl": row["backtranslated_nl"],
        }
    return scores


def validate_formula(parser, formula):
    try:
        parser.parse(formula)
        return True
    except Exception:
        return False


def pattern_ok(formula_type, formula):
    if formula_type == "implication":
        return "->" in formula
    return "|" in formula and "->" not in formula


def collect_rows(source, config, parser):
    ast_metrics = load_ast_metrics(config["ast_files"])
    roundtrip = load_roundtrip(config["roundtrip_file"])
    rows = []

    for path in config["stakeholder_files"]:
        for source_row in read_csv(path):
            for formula_type, column in FORMULA_COLUMNS.items():
                formula = source_row[column]
                key = (source_row["id"], formula_type)
                metric = ast_metrics.get(key, {})
                score = roundtrip.get(key, {})
                rows.append({
                    "source": source,
                    "id": source_row["id"],
                    "stakeholder": source_row["stakeholder"],
                    "norm_type": source_row["norm_type"],
                    "formula_type": formula_type,
                    "nl_norm": source_row["nl_norm"],
                    "formula": formula,
                    "parser_valid": validate_formula(parser, formula),
                    "expected_pattern": pattern_ok(formula_type, formula),
                    "auto_semantic_score": score.get("auto_semantic_score", ""),
                    "auto_error_type": score.get("auto_error_type", ""),
                    "ast_node_count": metric.get("ast_node_count", 0),
                    "ast_depth": metric.get("ast_depth", 0),
                    "ast_predicate_count": metric.get("ast_predicate_count", formula_predicate_count(formula)),
                })

    return rows


def summarize(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["source"], row["formula_type"])].append(row)

    summary = []
    for (source, formula_type), items in sorted(grouped.items()):
        scores = Counter(row["auto_semantic_score"] for row in items)
        summary.append({
            "source": source,
            "formula_type": formula_type,
            "formulas": len(items),
            "parser_valid": sum(row["parser_valid"] for row in items),
            "expected_pattern": sum(row["expected_pattern"] for row in items),
            "score_2": scores.get("2", 0),
            "score_1": scores.get("1", 0),
            "score_0": scores.get("0", 0),
            "avg_ast_nodes": average([row["ast_node_count"] for row in items]),
            "avg_ast_depth": average([row["ast_depth"] for row in items]),
            "avg_ast_predicates": average([row["ast_predicate_count"] for row in items]),
        })
    return summary


def paired_mismatches(rows):
    by_source_id = defaultdict(dict)
    for row in rows:
        by_source_id[(row["source"], row["id"])][row["formula_type"]] = row

    examples = []
    for (source, row_id), pair in sorted(by_source_id.items()):
        implication = pair.get("implication")
        dyadic = pair.get("dyadic")
        if not implication or not dyadic:
            continue
        implication_score = implication["auto_semantic_score"]
        dyadic_score = dyadic["auto_semantic_score"]
        if implication_score != dyadic_score:
            examples.append({
                "source": source,
                "id": row_id,
                "stakeholder": implication["stakeholder"],
                "norm_type": implication["norm_type"],
                "nl_norm": implication["nl_norm"],
                "implication_score": implication_score,
                "dyadic_score": dyadic_score,
                "implication_error_type": implication["auto_error_type"],
                "dyadic_error_type": dyadic["auto_error_type"],
                "implication_formula": implication["formula"],
                "dyadic_formula": dyadic["formula"],
            })
    return examples


def write_csv(path, rows, fieldnames=None):
    if not rows and not fieldnames:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(summary_rows, mismatch_rows):
    lines = [
        "# Implication vs Dyadic Formulation Comparison",
        "",
        "This report compares the paired implication-based and dyadic formulas generated for the same natural-language stakeholder norms.",
        "",
        "Implication formulas place the condition outside the deontic operator: `condition -> O(action)`.",
        "",
        "Dyadic formulas place the condition inside the deontic operator: `O(action | condition)`.",
        "",
        "## Aggregate Results",
        "",
        "| Source | Formula type | Formulas | Parser valid | Expected pattern | Score 2 | Score 1 | Score 0 | Avg AST nodes | Avg AST depth | Avg predicates |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for row in summary_rows:
        lines.append(
            f"| {row['source']} | {row['formula_type']} | {row['formulas']} | "
            f"{row['parser_valid']} | {row['expected_pattern']} | "
            f"{row['score_2']} | {row['score_1']} | {row['score_0']} | "
            f"{row['avg_ast_nodes']} | {row['avg_ast_depth']} | {row['avg_ast_predicates']} |"
        )

    lines.extend([
        "",
        "## Paired Round-Trip Score Differences",
        "",
        f"Rows where implication and dyadic formulas for the same norm received different automatic round-trip scores: {len(mismatch_rows)}.",
        "",
    ])

    if mismatch_rows:
        lines.extend([
            "| Source | ID | Stakeholder | Implication score | Dyadic score | Norm |",
            "|---|---|---|---:|---:|---|",
        ])
        for row in mismatch_rows[:20]:
            norm = row["nl_norm"].replace("|", "\\|")
            lines.append(
                f"| {row['source']} | {row['id']} | {row['stakeholder']} | "
                f"{row['implication_score']} | {row['dyadic_score']} | {norm} |"
            )
        lines.extend([
            "",
            "The complete mismatch list is stored in `outputs/comparison/formulation_type_mismatches.csv`.",
            "",
        ])

    lines.extend([
        "## Interpretation",
        "",
        "This comparison does not treat the two formula types as semantically identical. Instead, it evaluates how the two rival formalisation strategies behave when applied to the same natural-language norms.",
        "",
        "The key thesis use is to compare syntax compliance, round-trip semantic preservation, and AST-level structural complexity under controlled input conditions.",
    ])

    (OUT_DIR / "formulation_type_comparison.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    parser = load_parser()

    rows = []
    for source, config in DATASETS.items():
        rows.extend(collect_rows(source, config, parser))

    summary_rows = summarize(rows)
    mismatch_rows = paired_mismatches(rows)

    write_csv(OUT_DIR / "formulation_type_formula_metrics.csv", rows)
    write_csv(OUT_DIR / "formulation_type_comparison.csv", summary_rows)
    write_csv(
        OUT_DIR / "formulation_type_mismatches.csv",
        mismatch_rows,
        fieldnames=[
            "source",
            "id",
            "stakeholder",
            "norm_type",
            "nl_norm",
            "implication_score",
            "dyadic_score",
            "implication_error_type",
            "dyadic_error_type",
            "implication_formula",
            "dyadic_formula",
        ],
    )
    write_markdown(summary_rows, mismatch_rows)

    print(f"Wrote formulation-type comparison outputs to {OUT_DIR}")


if __name__ == "__main__":
    main()
