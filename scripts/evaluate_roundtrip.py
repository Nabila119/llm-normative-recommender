import csv
import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROUNDTRIP_DIR = PROJECT_ROOT / "outputs" / "roundtrip"
INPUT = ROUNDTRIP_DIR / "roundtrip_backtranslations.csv"
CSV_OUT = ROUNDTRIP_DIR / "roundtrip_evaluated.csv"
JSON_OUT = ROUNDTRIP_DIR / "roundtrip_evaluated.json"


MODALITY_CUES = {
    "obligation": [
        "should",
        "must",
        "requires",
        "required",
        "obligated",
        "receive",
        "recommended",
        "be recommended",
    ],
    "permission": [
        "may",
        "can",
        "permitted",
        "allowed",
    ],
    "prohibition": [
        "should not",
        "must not",
        "not receive",
        "prohibited",
        "forbidden",
        "not be recommended",
        "shouldn't",
        "cannot",
    ],
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "be",
    "by",
    "for",
    "food",
    "foods",
    "from",
    "if",
    "in",
    "is",
    "it",
    "meal",
    "meals",
    "must",
    "not",
    "of",
    "or",
    "product",
    "products",
    "recommend",
    "recommendation",
    "recommendations",
    "recommended",
    "recommender",
    "receive",
    "rule",
    "safety",
    "should",
    "system",
    "that",
    "the",
    "then",
    "this",
    "to",
    "user",
    "users",
    "when",
    "with",
}

SYNONYM_GROUPS = [
    {"child", "children"},
    {"adult", "adults"},
    {"elderly"},
    {"diabetic", "diabetes"},
    {"hypertensive", "hypertension"},
    {"pregnant", "pregnancy"},
    {"halal"},
    {"kosher"},
    {"gluten", "glutenfree"},
    {"lactose", "dairy"},
    {"shellfish"},
    {"nut", "nuts"},
    {"vegan", "nonvegan"},
    {"vegetarian", "nonvegetarian"},
    {"energy", "drink"},
    {"sugar", "sugary"},
    {"salt", "salty"},
    {"fat"},
    {"organic"},
    {"sustainable", "sustainability"},
    {"affordable", "budget", "discounted"},
    {"spicy"},
    {"mild"},
    {"mediterranean"},
    {"asian"},
    {"sponsored"},
    {"premium"},
    {"certified", "certification"},
    {"approved", "approval"},
    {"restricted", "restriction"},
    {"warning", "warnings"},
    {"label", "labels", "labeling"},
    {"allergen", "allergens", "allergic"},
    {"available", "availability"},
    {"local"},
    {"seasonal"},
]


def normalize_text(text):
    text = text.lower()
    text = text.replace("-", "")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokens(text):
    return {
        token
        for token in normalize_text(text).split()
        if len(token) > 2 and token not in STOPWORDS
    }


def modality_matches(original, norm_type):
    text = normalize_text(original)
    cues = MODALITY_CUES.get(norm_type, [])
    return any(cue in text for cue in cues)


def concept_matches(original, backtranslation):
    original_tokens = tokens(original)
    back_tokens = tokens(backtranslation)
    direct = original_tokens & back_tokens

    concept_hits = set()
    original_concepts = set()
    for index, group in enumerate(SYNONYM_GROUPS):
        if original_tokens & group:
            original_concepts.add(index)
            if back_tokens & group:
                concept_hits.add(index)

    return {
        "original_tokens": sorted(original_tokens),
        "back_tokens": sorted(back_tokens),
        "direct_overlap": sorted(direct),
        "original_concepts": len(original_concepts),
        "concept_hits": len(concept_hits),
    }


def evaluate_row(row):
    original = row["original_nl"]
    back = row["backtranslated_nl"]
    norm_type = row["norm_type"]

    modality_ok = modality_matches(original, norm_type)
    match = concept_matches(original, back)

    original_concepts = match["original_concepts"]
    concept_hits = match["concept_hits"]
    direct_overlap = len(match["direct_overlap"])

    if original_concepts:
        concept_ratio = concept_hits / original_concepts
    else:
        concept_ratio = 1.0 if direct_overlap else 0.0

    if modality_ok and concept_ratio >= 0.75:
        score = "2"
        error_type = "none"
        notes = "Automatic check found modality agreement and strong concept overlap."
    elif modality_ok and (concept_ratio >= 0.4 or direct_overlap >= 1):
        score = "1"
        error_type = "partial_concept_overlap"
        notes = "Automatic check found modality agreement but only partial concept overlap."
    elif not modality_ok and concept_ratio >= 0.75:
        score = "1"
        error_type = "modality_uncertain"
        notes = "Automatic check found concept overlap but could not confirm modality from the original text."
    else:
        score = "0"
        error_type = "semantic_mismatch_possible"
        notes = "Automatic check found weak modality or concept agreement; human review needed."

    return {
        "auto_semantic_score": score,
        "auto_error_type": error_type,
        "auto_notes": notes,
        "auto_direct_overlap": ";".join(match["direct_overlap"]),
        "auto_original_concepts": str(original_concepts),
        "auto_concept_hits": str(concept_hits),
        "human_semantic_score": "",
        "human_error_type": "",
        "human_notes": "",
    }


def main():
    with INPUT.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    evaluated = []
    for row in rows:
        clean_row = {
            "id": row["id"],
            "stakeholder": row["stakeholder"],
            "formula_type": row["formula_type"],
            "norm_type": row["norm_type"],
            "original_nl": row["original_nl"],
            "formula": row["formula"],
            "backtranslated_nl": row["backtranslated_nl"],
        }
        clean_row.update(evaluate_row(row))
        evaluated.append(clean_row)

    fieldnames = [
        "id",
        "stakeholder",
        "formula_type",
        "norm_type",
        "original_nl",
        "formula",
        "backtranslated_nl",
        "auto_semantic_score",
        "auto_error_type",
        "auto_notes",
        "auto_direct_overlap",
        "auto_original_concepts",
        "auto_concept_hits",
        "human_semantic_score",
        "human_error_type",
        "human_notes",
    ]

    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(evaluated)

    JSON_OUT.write_text(json.dumps(evaluated, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = {}
    for row in evaluated:
        key = row["auto_semantic_score"]
        counts[key] = counts.get(key, 0) + 1

    print(f"evaluated rows={len(evaluated)}")
    print(f"auto score counts={counts}")
    print(f"csv={CSV_OUT}")
    print(f"json={JSON_OUT}")


if __name__ == "__main__":
    main()
