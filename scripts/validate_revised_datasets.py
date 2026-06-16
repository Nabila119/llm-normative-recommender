import argparse
import csv
from pathlib import Path

from lark import Lark


PROJECT_ROOT = Path(__file__).resolve().parents[1]

STAKEHOLDER_HEADER = [
    "id",
    "stakeholder",
    "nl_norm",
    "implication_formula",
    "dyadic_formula",
    "norm_type",
]

CONSTITUTIVE_HEADER = [
    "id",
    "scope",
    "nl_rule",
    "logic_rule",
    "category",
]

VALID_NORM_TYPES = {"obligation", "permission", "prohibition"}


def load_parser():
    grammar = (PROJECT_ROOT / "grammar" / "grammar.lark").read_text(encoding="utf-8")
    return Lark(grammar, start="formula", parser="lalr")


def project_path(value):
    path = Path(value)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def check_parse(parser, formula, location, errors):
    try:
        parser.parse(formula)
    except Exception as exc:
        first_line = str(exc).splitlines()[0] if str(exc) else repr(exc)
        errors.append(f"{location}: parse error: {first_line}: {formula}")


def check_unique(rows, field, label, errors):
    seen = {}
    for row in rows:
        value = row.get(field, "")
        if value in seen:
            errors.append(f"{label}: duplicate {field} {value!r} also seen in {seen[value]}")
        else:
            seen[value] = row.get("id", "<no id>")


def validate_stakeholder_file(path, parser):
    errors = []
    warnings = []
    header, rows = read_csv(path)

    if header != STAKEHOLDER_HEADER:
        errors.append(f"{path.name}: expected header {STAKEHOLDER_HEADER}, got {header}")

    check_unique(rows, "id", path.name, errors)
    check_unique(rows, "nl_norm", path.name, errors)
    check_unique(rows, "implication_formula", path.name, errors)
    check_unique(rows, "dyadic_formula", path.name, errors)

    for index, row in enumerate(rows, start=2):
        row_id = row.get("id", f"line {index}")
        norm_type = row.get("norm_type", "")
        implication = row.get("implication_formula", "")
        dyadic = row.get("dyadic_formula", "")

        if norm_type not in VALID_NORM_TYPES:
            errors.append(f"{path.name}:{row_id}: invalid norm_type {norm_type!r}")

        check_parse(parser, implication, f"{path.name}:{row_id}:implication_formula", errors)
        check_parse(parser, dyadic, f"{path.name}:{row_id}:dyadic_formula", errors)

        if "recommend(System,y,x)" not in implication:
            errors.append(f"{path.name}:{row_id}: implication_formula must use recommend(System,y,x)")
        if "recommend(System,y,x)" not in dyadic:
            errors.append(f"{path.name}:{row_id}: dyadic_formula must use recommend(System,y,x)")

        if not implication.startswith("∀x.∀y."):
            errors.append(f"{path.name}:{row_id}: implication_formula must start with ∀x.∀y.")
        if not dyadic.startswith("∀x.∀y."):
            errors.append(f"{path.name}:{row_id}: dyadic_formula must start with ∀x.∀y.")

        if "->" not in implication:
            errors.append(f"{path.name}:{row_id}: implication_formula must contain ->")
        if "|" not in dyadic:
            errors.append(f"{path.name}:{row_id}: dyadic_formula must contain |")

        if any(old in implication or old in dyadic for old in ["recommend(System,EnergyDrink)", "recommend(System,GlutenFreeMeal)", "recommend(System,LowSugarFood)"]):
            errors.append(f"{path.name}:{row_id}: formula appears to use old constant-based recommendation style")

        if row.get("stakeholder", "") not in {"User", "Food Ministry", "Food Industry"}:
            warnings.append(f"{path.name}:{row_id}: unusual stakeholder {row.get('stakeholder', '')!r}")

    return rows, errors, warnings


def validate_constitutive_file(path, parser):
    errors = []
    warnings = []
    header, rows = read_csv(path)

    if header != CONSTITUTIVE_HEADER:
        errors.append(f"{path.name}: expected header {CONSTITUTIVE_HEADER}, got {header}")

    check_unique(rows, "id", path.name, errors)
    check_unique(rows, "nl_rule", path.name, errors)
    check_unique(rows, "logic_rule", path.name, errors)

    for index, row in enumerate(rows, start=2):
        row_id = row.get("id", f"line {index}")
        rule = row.get("logic_rule", "")

        check_parse(parser, rule, f"{path.name}:{row_id}:logic_rule", errors)

        if not rule.startswith("∀y."):
            errors.append(f"{path.name}:{row_id}: logic_rule must start with ∀y.")
        if "->" not in rule:
            errors.append(f"{path.name}:{row_id}: logic_rule must contain ->")
        if "recommend(" in rule:
            errors.append(f"{path.name}:{row_id}: constitutive rules must not contain recommend(...)")
        if any(modal in rule for modal in ["O(", "P(", "F("]):
            errors.append(f"{path.name}:{row_id}: constitutive rules must not contain modal operators")

        if row.get("scope", "") != "FoodDomain":
            warnings.append(f"{path.name}:{row_id}: unusual scope {row.get('scope', '')!r}")

    return rows, errors, warnings


def main():
    parser_arg = argparse.ArgumentParser(description="Validate revised stakeholder norm datasets.")
    parser_arg.add_argument(
        "--stakeholder",
        nargs="*",
        default=[
            "data/revised/user_dataset.csv",
            "data/revised/food_ministry_dataset.csv",
            "data/revised/food_industry_dataset.csv",
        ],
        help="Stakeholder dataset CSV files.",
    )
    parser_arg.add_argument(
        "--constitutive",
        nargs="*",
        default=["data/revised/constitutive_rules.csv"],
        help="Constitutive rule CSV files.",
    )
    args = parser_arg.parse_args()

    parser = load_parser()
    all_errors = []
    all_warnings = []
    total_rows = 0
    total_formulas = 0

    for filename in args.stakeholder:
        path = project_path(filename)
        rows, errors, warnings = validate_stakeholder_file(path, parser)
        total_rows += len(rows)
        total_formulas += len(rows) * 2
        all_errors.extend(errors)
        all_warnings.extend(warnings)
        print(f"{filename}: rows={len(rows)} formulas={len(rows) * 2} errors={len(errors)} warnings={len(warnings)}")

    for filename in args.constitutive:
        path = project_path(filename)
        rows, errors, warnings = validate_constitutive_file(path, parser)
        total_rows += len(rows)
        total_formulas += len(rows)
        all_errors.extend(errors)
        all_warnings.extend(warnings)
        print(f"{filename}: rows={len(rows)} formulas={len(rows)} errors={len(errors)} warnings={len(warnings)}")

    print(f"TOTAL: rows={total_rows} formulas={total_formulas} errors={len(all_errors)} warnings={len(all_warnings)}")

    if all_warnings:
        print("\nWARNINGS")
        for warning in all_warnings:
            print(f"- {warning}")

    if all_errors:
        print("\nERRORS")
        for error in all_errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
