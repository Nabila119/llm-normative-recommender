import argparse
import csv
import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AST_DIR = PROJECT_ROOT / "outputs" / "asts"
OUT_DIR = PROJECT_ROOT / "outputs" / "roundtrip"

STAKEHOLDER_AST_FILES = [
    "revised_user_asts.json",
    "revised_food_ministry_asts.json",
    "revised_food_industry_asts.json",
]

USER_TERMS = {
    "x": "the user",
}

PRODUCT_TERMS = {
    "y": "the product",
}

CONSTANT_LABELS = {
    "Asian": "Asian cuisine",
    "CuisineSpecific": "cuisine-specific products",
    "DiscountedFood": "discounted food",
    "Gluten": "gluten",
    "Lactose": "lactose",
    "LocalFood": "local food",
    "MarketPreference": "market-preference products",
    "Mediterranean": "Mediterranean cuisine",
    "NewProduct": "new products",
    "Nuts": "nuts",
    "SeasonalFood": "seasonal food",
    "Shellfish": "shellfish",
    "SpicyFood": "spicy food",
    "SustainableFood": "sustainable food",
}

PREDICATE_TEMPLATES = {
    "adult": "the user is an adult",
    "affordable": "the product is affordable",
    "affordableMeal": "the product is an affordable meal",
    "ageRestrictedProduct": "the product is age-restricted",
    "allergenSafeMeal": "the product is allergen-safe",
    "allergicTo": "the user is allergic to {1}",
    "alternativeToRestrictedFood": "the product is an alternative to restricted food",
    "approved": "the product is approved",
    "approvedByMinistry": "the product is approved by the ministry",
    "asianMeal": "the product is an Asian meal",
    "available": "the product is available",
    "avoids": "the user avoids the product",
    "bannedForChildren": "the product is banned for children",
    "brandSafe": "the product is brand-safe",
    "brandUnsafe": "the product is brand-unsafe",
    "caffeinatedProduct": "the product is caffeinated",
    "certified": "the product is certified",
    "certifiedGlutenFree": "the product is certified gluten-free",
    "certifiedHalal": "the product is certified halal",
    "certifiedHealthy": "the product is certified healthy",
    "certifiedKosher": "the product is certified kosher",
    "certifiedLactoseFree": "the product is certified lactose-free",
    "child": "the user is a child",
    "completeLabel": "the product has a complete label",
    "compliesWithGuideline": "the product complies with ministry guidelines",
    "compliesWithLabeling": "the product complies with labeling rules",
    "contains": "the product contains {1}",
    "containsUndeclaredAllergen": "the product contains an undeclared allergen",
    "cuisineSpecificProduct": "the product is cuisine-specific",
    "dairyMeal": "the product is a dairy meal",
    "diabetic": "the user is diabetic",
    "discounted": "the product is discounted",
    "discountedMeal": "the product is a discounted meal",
    "eggMeal": "the product is an egg meal",
    "elderly": "the user is elderly",
    "eligible": "the user is eligible",
    "energyDrink": "the product is an energy drink",
    "environmentFriendly": "the product is environmentally friendly",
    "essentialFood": "the product is essential food",
    "exceedsFatLimit": "the product exceeds fat limits",
    "exceedsSaltLimit": "the product exceeds salt limits",
    "exceedsSugarLimit": "the product exceeds sugar limits",
    "freshMeal": "the product is a fresh meal",
    "friedMeal": "the product is a fried meal",
    "glutenFreeMeal": "the product is a gluten-free meal",
    "glutenSensitive": "the user is gluten-sensitive",
    "hasAllergenLabel": "the product has an allergen label",
    "hasHealthGoal": "the user has a health goal",
    "hasNutritionLabel": "the product has a nutrition label",
    "hasSafetyWarning": "the product has a safety warning",
    "halalMeal": "the product is a halal meal",
    "healthyMeal": "the product is a healthy meal",
    "heartHealthyMeal": "the product is a heart-healthy meal",
    "highFatProduct": "the product is high in fat",
    "highSaltProduct": "the product is high in salt",
    "highSugarProduct": "the product is high in sugar",
    "hypertensive": "the user is hypertensive",
    "incompleteLabel": "the product has an incomplete label",
    "interestedIn": "the user is interested in {1}",
    "kosherMeal": "the product is a kosher meal",
    "lactoseFreeMeal": "the product is a lactose-free meal",
    "lactoseIntolerant": "the user is lactose-intolerant",
    "localProduct": "the product is local",
    "lowFatMeal": "the product is a low-fat meal",
    "lowSaltFood": "the product is low in salt",
    "lowSugarFood": "the product is low in sugar",
    "loyalCustomer": "the user is a loyal customer",
    "marketPreferenceProduct": "the product is a market-preference product",
    "meatMeal": "the product is a meat meal",
    "mediterraneanMeal": "the product is a Mediterranean meal",
    "meetsNutritionGuideline": "the product meets nutrition guidelines",
    "mild": "the product is mild",
    "mildMeal": "the product is a mild meal",
    "misleadingClaim": "the product has a misleading claim",
    "newProduct": "the product is new",
    "nonHalal": "the product is non-halal",
    "nonKosher": "the product is non-kosher",
    "nonVegan": "the product is non-vegan",
    "nonVegetarian": "the product is non-vegetarian",
    "nutFreeMeal": "the product is nut-free",
    "nutSnack": "the product is a nut snack",
    "organic": "the product is organic",
    "organicFood": "the product is organic food",
    "plantBasedMeal": "the product is plant-based",
    "pregnant": "the user is pregnant",
    "premiumCustomer": "the user is a premium customer",
    "premiumProduct": "the product is premium",
    "prefers": "the user prefers the product",
    "processedMeat": "the product is processed meat",
    "proteinRichMeal": "the product is protein-rich",
    "requiresCertifiedProduct": "the user requires certified products",
    "requiresGlutenFree": "the user requires gluten-free food",
    "requiresHalal": "the user requires halal food",
    "requiresHeartHealthy": "the user requires heart-healthy food",
    "requiresKosher": "the user requires kosher food",
    "requiresLactoseFree": "the user requires lactose-free food",
    "requiresLowSalt": "the user requires low-salt food",
    "requiresLowSugar": "the user requires low-sugar food",
    "requiresWarning": "the product requires a warning",
    "restricted": "the product is restricted",
    "safeFor": "the product is safe for the user",
    "safeForDiabeticUsers": "the product is safe for diabetic users",
    "safeForPregnantUsers": "the product is safe for pregnant users",
    "safetyWarningProduct": "the product has a safety warning",
    "saltySnack": "the product is a salty snack",
    "seasonal": "the product is seasonal",
    "seasonalMeal": "the product is a seasonal meal",
    "shellfishFreeMeal": "the product is shellfish-free",
    "shellfishMeal": "the product is a shellfish meal",
    "spicy": "the product is spicy",
    "spicyMeal": "the product is a spicy meal",
    "sponsored": "the product is sponsored",
    "sugarySnack": "the product is a sugary snack",
    "suitableForChildren": "the product is suitable for children",
    "sustainable": "the product is sustainable",
    "ultraProcessedFood": "the product is ultra-processed",
    "unaffordable": "the product is unaffordable",
    "uncertainHalalStatus": "the product has uncertain halal status",
    "uncertainKosherStatus": "the product has uncertain kosher status",
    "underage": "the user is underage",
    "unsafeProduct": "the product is unsafe",
    "unsuitableForChildren": "the product is unsuitable for children",
    "vegan": "the user is vegan",
    "veganMeal": "the product is a vegan meal",
    "vegetarian": "the user is vegetarian",
    "vegetarianMeal": "the product is a vegetarian meal",
    "verifiedClaim": "the product has a verified claim",
    "verifiedHalal": "the product has verified halal status",
    "verifiedKosher": "the product has verified kosher status",
    "vulnerableUser": "the user is vulnerable",
    "wheatMeal": "the product is a wheat meal",
}

MODALITY_TEXT = {
    "O": "the system is obligated to recommend the product to the user",
    "P": "the system is permitted to recommend the product to the user",
    "F": "the system is prohibited from recommending the product to the user",
}


def split_predicate(expr):
    match = re.fullmatch(r"¬?([A-Za-z][A-Za-z0-9]*)\((.*)\)", expr)
    if not match:
        return None, []
    name = match.group(1)
    args = [arg.strip() for arg in match.group(2).split(",") if arg.strip()]
    return name, args


def label_arg(arg):
    return USER_TERMS.get(arg) or PRODUCT_TERMS.get(arg) or CONSTANT_LABELS.get(arg) or camel_to_words(arg)


def camel_to_words(value):
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    return value.replace("  ", " ").lower()


def condition_to_english(condition):
    negated = condition.startswith("¬")
    raw = condition[1:] if negated else condition
    name, args = split_predicate(raw)

    if name in PREDICATE_TEMPLATES:
        template = PREDICATE_TEMPLATES[name]
        text = template
        for index, arg in enumerate(args):
            text = text.replace(f"{{{index}}}", label_arg(arg))
    elif name:
        rendered_args = ", ".join(label_arg(arg) for arg in args)
        text = f"{camel_to_words(name)} holds for {rendered_args}" if rendered_args else camel_to_words(name)
    else:
        text = raw

    if negated:
        return f"it is not the case that {text}"
    return text


def backtranslate_norm(normalized):
    conditions = normalized.get("condition", [])
    modality = normalized.get("modality", "")
    modality_text = MODALITY_TEXT.get(modality, f"the system has modality {modality} for recommending the product to the user")

    if conditions:
        condition_text = " and ".join(condition_to_english(condition) for condition in conditions)
        return f"For every user and product, if {condition_text}, then {modality_text}."

    return f"For every user and product, {modality_text}."


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_roundtrip_rows(ast_files):
    rows = []
    for ast_file in ast_files:
        records = read_json(AST_DIR / ast_file)
        for record in records:
            for formula_type, normalized_key, formula_key in [
                ("implication", "normalized_implication", "implication_formula"),
                ("dyadic", "normalized_dyadic", "dyadic_formula"),
            ]:
                normalized = record[normalized_key]
                rows.append({
                    "id": record["id"],
                    "stakeholder": record["stakeholder"],
                    "formula_type": formula_type,
                    "norm_type": record["norm_type"],
                    "original_nl": record["nl_norm"],
                    "formula": record[formula_key],
                    "backtranslated_nl": backtranslate_norm(normalized),
                    "semantic_score": "",
                    "error_type": "",
                    "notes": "",
                })
    return rows


def write_csv(path, rows):
    fieldnames = [
        "id",
        "stakeholder",
        "formula_type",
        "norm_type",
        "original_nl",
        "formula",
        "backtranslated_nl",
        "semantic_score",
        "error_type",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Generate round-trip backtranslations from normalized ASTs.")
    parser.add_argument("--ast-files", nargs="*", default=STAKEHOLDER_AST_FILES)
    parser.add_argument("--csv", default="roundtrip_backtranslations.csv")
    parser.add_argument("--json", default="roundtrip_backtranslations.json")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = build_roundtrip_rows(args.ast_files)
    write_csv(OUT_DIR / args.csv, rows)
    write_json(OUT_DIR / args.json, rows)

    print(f"roundtrip rows={len(rows)}")
    print(f"csv={OUT_DIR / args.csv}")
    print(f"json={OUT_DIR / args.json}")


if __name__ == "__main__":
    main()
