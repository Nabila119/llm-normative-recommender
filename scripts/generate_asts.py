import argparse
import csv
import json
from pathlib import Path

from lark import Lark, Token, Tree


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT_ROOT / "outputs" / "asts"

STAKEHOLDER_FILES = [
    ("data/revised/user_dataset.csv", "revised_user_asts.json"),
    ("data/revised/food_ministry_dataset.csv", "revised_food_ministry_asts.json"),
    ("data/revised/food_industry_dataset.csv", "revised_food_industry_asts.json"),
]

CONSTITUTIVE_FILES = [
    ("data/revised/constitutive_rules.csv", "constitutive_rule_asts.json"),
]


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
        return list(csv.DictReader(f))


def flatten_term_list(node):
    if isinstance(node, Token):
        return [str(node)]
    if isinstance(node, Tree):
        if node.data == "atomic_term":
            return [str(node.children[0])]
        if node.data == "function_term":
            name = str(node.children[0])
            args = flatten_term_list(node.children[1])
            return [{"type": "function", "name": name, "args": args}]
        if node.data == "term_list":
            terms = []
            for child in node.children:
                terms.extend(flatten_term_list(child))
            return terms
    return [to_ast(node)]


def to_ast(node):
    if isinstance(node, Token):
        return str(node)

    if not isinstance(node, Tree):
        return node

    data = node.data
    children = node.children

    if data in {"forall", "exists"}:
        return {
            "type": "quantifier",
            "quantifier": "forall" if data == "forall" else "exists",
            "variable": str(children[0]),
            "body": to_ast(children[1]),
        }

    if data == "implication":
        return {
            "type": "implication",
            "antecedent": to_ast(children[0]),
            "consequent": to_ast(children[1]),
        }

    if data == "disjunction":
        return {
            "type": "or",
            "children": [to_ast(children[0]), to_ast(children[1])],
        }

    if data == "conjunction":
        return {
            "type": "and",
            "children": [to_ast(children[0]), to_ast(children[1])],
        }

    if data == "negation":
        return {
            "type": "not",
            "body": to_ast(children[0]),
        }

    if data == "modal_formula":
        operator = str(children[0])
        if len(children) == 2:
            return {
                "type": "modal",
                "operator": operator,
                "formula": to_ast(children[1]),
            }
        return {
            "type": "modal",
            "operator": operator,
            "formula": to_ast(children[1]),
            "condition": to_ast(children[2]),
        }

    if data == "predicate":
        name = str(children[0])
        args = flatten_term_list(children[1]) if len(children) > 1 else []
        return {
            "type": "predicate",
            "name": name,
            "args": args,
        }

    if data == "function_term":
        return {
            "type": "function",
            "name": str(children[0]),
            "args": flatten_term_list(children[1]),
        }

    if data == "atomic_term":
        return str(children[0])

    if data == "term_list":
        return flatten_term_list(node)

    if len(children) == 1:
        return to_ast(children[0])

    return {
        "type": data,
        "children": [to_ast(child) for child in children],
    }


def strip_quantifiers(ast):
    variables = []
    current = ast
    while isinstance(current, dict) and current.get("type") == "quantifier":
        variables.append({
            "quantifier": current["quantifier"],
            "variable": current["variable"],
        })
        current = current["body"]
    return variables, current


def expr_to_string(expr):
    if isinstance(expr, str):
        return expr
    if not isinstance(expr, dict):
        return str(expr)

    expr_type = expr.get("type")

    if expr_type == "predicate":
        args = ",".join(expr_to_string(arg) for arg in expr.get("args", []))
        return f"{expr['name']}({args})" if args else expr["name"]

    if expr_type == "function":
        args = ",".join(expr_to_string(arg) for arg in expr.get("args", []))
        return f"{expr['name']}({args})"

    if expr_type == "and":
        return "∧".join(expr_to_string(child) for child in flatten_logical(expr, "and"))

    if expr_type == "or":
        return "∨".join(expr_to_string(child) for child in flatten_logical(expr, "or"))

    if expr_type == "not":
        return f"¬{expr_to_string(expr['body'])}"

    if expr_type == "modal":
        formula = expr_to_string(expr["formula"])
        if "condition" in expr:
            return f"{expr['operator']}({formula}|{expr_to_string(expr['condition'])})"
        return f"{expr['operator']}({formula})"

    if expr_type == "implication":
        return f"{expr_to_string(expr['antecedent'])}->{expr_to_string(expr['consequent'])}"

    if expr_type == "quantifier":
        symbol = "∀" if expr["quantifier"] == "forall" else "∃"
        return f"{symbol}{expr['variable']}.{expr_to_string(expr['body'])}"

    return json.dumps(expr, ensure_ascii=False, sort_keys=True)


def flatten_logical(expr, kind):
    if isinstance(expr, dict) and expr.get("type") == kind:
        items = []
        for child in expr.get("children", []):
            items.extend(flatten_logical(child, kind))
        return items
    return [expr]


def condition_to_list(expr):
    if expr is None:
        return []
    if isinstance(expr, dict) and expr.get("type") == "and":
        return sorted(expr_to_string(item) for item in flatten_logical(expr, "and"))
    return [expr_to_string(expr)]


def normalize_norm_ast(ast):
    quantifiers, body = strip_quantifiers(ast)

    if isinstance(body, dict) and body.get("type") == "implication":
        consequent = body["consequent"]
        if isinstance(consequent, dict) and consequent.get("type") == "modal":
            return {
                "quantifiers": quantifiers,
                "form": "implication",
                "modality": consequent["operator"],
                "action": expr_to_string(consequent["formula"]),
                "condition": condition_to_list(body["antecedent"]),
            }

    if isinstance(body, dict) and body.get("type") == "modal":
        return {
            "quantifiers": quantifiers,
            "form": "dyadic" if "condition" in body else "monadic",
            "modality": body["operator"],
            "action": expr_to_string(body["formula"]),
            "condition": condition_to_list(body.get("condition")),
        }

    return {
        "quantifiers": quantifiers,
        "form": "unknown",
        "raw": expr_to_string(body),
    }


def normalize_constitutive_ast(ast):
    quantifiers, body = strip_quantifiers(ast)

    if isinstance(body, dict) and body.get("type") == "implication":
        return {
            "quantifiers": quantifiers,
            "if": condition_to_list(body["antecedent"]),
            "then": expr_to_string(body["consequent"]),
        }

    return {
        "quantifiers": quantifiers,
        "raw": expr_to_string(body),
    }


def parse_to_ast(parser, formula):
    tree = parser.parse(formula)
    return to_ast(tree)


def generate_stakeholder_asts(parser, csv_name, output_name):
    records = []
    for row in read_csv(project_path(csv_name)):
        implication_ast = parse_to_ast(parser, row["implication_formula"])
        dyadic_ast = parse_to_ast(parser, row["dyadic_formula"])
        records.append({
            "id": row["id"],
            "stakeholder": row["stakeholder"],
            "nl_norm": row["nl_norm"],
            "norm_type": row["norm_type"],
            "implication_formula": row["implication_formula"],
            "dyadic_formula": row["dyadic_formula"],
            "implication_ast": implication_ast,
            "dyadic_ast": dyadic_ast,
            "normalized_implication": normalize_norm_ast(implication_ast),
            "normalized_dyadic": normalize_norm_ast(dyadic_ast),
        })

    write_json(output_name, records)
    return len(records)


def generate_constitutive_asts(parser, csv_name, output_name):
    records = []
    for row in read_csv(project_path(csv_name)):
        ast = parse_to_ast(parser, row["logic_rule"])
        records.append({
            "id": row["id"],
            "scope": row["scope"],
            "nl_rule": row["nl_rule"],
            "category": row["category"],
            "logic_rule": row["logic_rule"],
            "ast": ast,
            "normalized_rule": normalize_constitutive_ast(ast),
        })

    write_json(output_name, records)
    return len(records)


def write_json(output_name, records):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / output_name
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    arg_parser = argparse.ArgumentParser(description="Generate AST JSON files for revised datasets.")
    arg_parser.add_argument("--stakeholder", nargs="*", default=None)
    arg_parser.add_argument("--constitutive", nargs="*", default=None)
    args = arg_parser.parse_args()

    parser = load_parser()
    total = 0

    stakeholder_files = STAKEHOLDER_FILES
    if args.stakeholder:
        stakeholder_files = [(name, f"{Path(name).stem}_asts.json") for name in args.stakeholder]

    constitutive_files = CONSTITUTIVE_FILES
    if args.constitutive:
        constitutive_files = [(name, f"{Path(name).stem}_asts.json") for name in args.constitutive]

    for csv_name, output_name in stakeholder_files:
        count = generate_stakeholder_asts(parser, csv_name, output_name)
        total += count
        print(f"{csv_name} -> outputs/asts/{output_name}: records={count}")

    for csv_name, output_name in constitutive_files:
        count = generate_constitutive_asts(parser, csv_name, output_name)
        total += count
        print(f"{csv_name} -> outputs/asts/{output_name}: records={count}")

    print(f"TOTAL AST RECORDS: {total}")


if __name__ == "__main__":
    main()
