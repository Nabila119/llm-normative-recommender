import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT = PROJECT_ROOT / "data" / "revised" / "food_ministry_dataset.csv"

MODAL = {
    "obligation": "O",
    "permission": "P",
    "prohibition": "F",
}


ROWS = [
    ("Children must not receive products exceeding sugar limits", "child(x)∧exceedsSugarLimit(y)", "prohibition"),
    ("Children must not receive age restricted products", "child(x)∧ageRestrictedProduct(y)", "prohibition"),
    ("Children must receive healthy meal recommendations when available", "child(x)∧healthyMeal(y)∧available(y)", "obligation"),
    ("Children may receive approved low sugar products", "child(x)∧approvedByMinistry(y)∧lowSugarFood(y)", "permission"),
    ("Children must not receive products requiring safety warnings", "child(x)∧requiresWarning(y)", "prohibition"),
    ("Diabetic users must receive foods safe for diabetic users", "diabetic(x)∧safeForDiabeticUsers(y)", "obligation"),
    ("Diabetic users must not receive products exceeding sugar limits", "diabetic(x)∧exceedsSugarLimit(y)", "prohibition"),
    ("Diabetic users may receive approved low sugar foods", "diabetic(x)∧approvedByMinistry(y)∧lowSugarFood(y)", "permission"),
    ("Diabetic users must receive foods with nutrition labels", "diabetic(x)∧hasNutritionLabel(y)", "obligation"),
    ("Diabetic users must not receive high sugar products", "diabetic(x)∧highSugarProduct(y)", "prohibition"),
    ("Hypertensive users must receive low salt foods", "hypertensive(x)∧lowSaltFood(y)", "obligation"),
    ("Hypertensive users must not receive products exceeding salt limits", "hypertensive(x)∧exceedsSaltLimit(y)", "prohibition"),
    ("Hypertensive users may receive approved low salt foods", "hypertensive(x)∧approvedByMinistry(y)∧lowSaltFood(y)", "permission"),
    ("Hypertensive users must receive foods complying with nutrition guidelines", "hypertensive(x)∧compliesWithGuideline(y)", "obligation"),
    ("Hypertensive users must not receive high salt products", "hypertensive(x)∧highSaltProduct(y)", "prohibition"),
    ("Pregnant users must receive foods safe for pregnant users", "pregnant(x)∧safeForPregnantUsers(y)", "obligation"),
    ("Pregnant users must not receive products requiring warnings", "pregnant(x)∧requiresWarning(y)", "prohibition"),
    ("Pregnant users may receive approved healthy meals", "pregnant(x)∧approvedByMinistry(y)∧healthyMeal(y)", "permission"),
    ("Pregnant users must receive products with safety information", "pregnant(x)∧hasSafetyWarning(y)", "obligation"),
    ("Pregnant users must not receive unsafe products", "pregnant(x)∧unsafeProduct(y)", "prohibition"),
    ("Elderly users must receive healthy meal recommendations", "elderly(x)∧healthyMeal(y)", "obligation"),
    ("Elderly users must not receive products exceeding salt limits", "elderly(x)∧exceedsSaltLimit(y)", "prohibition"),
    ("Elderly users may receive low sugar foods", "elderly(x)∧lowSugarFood(y)", "permission"),
    ("Elderly users must receive affordable healthy foods", "elderly(x)∧affordableMeal(y)∧healthyMeal(y)", "obligation"),
    ("Elderly users must not receive high fat products", "elderly(x)∧highFatProduct(y)", "prohibition"),
    ("Users allergic to nuts must not receive products containing nuts", "allergicTo(x,Nuts)∧contains(y,Nuts)", "prohibition"),
    ("Users allergic to shellfish must not receive products containing shellfish", "allergicTo(x,Shellfish)∧contains(y,Shellfish)", "prohibition"),
    ("Allergic users must receive products with allergen labels", "allergicTo(x,Nuts)∧hasAllergenLabel(y)", "obligation"),
    ("Allergic users may receive allergen safe products", "allergicTo(x,Nuts)∧allergenSafeMeal(y)", "permission"),
    ("Users with shellfish allergies must receive shellfish free products", "allergicTo(x,Shellfish)∧shellfishFreeMeal(y)", "obligation"),
    ("Products containing undeclared allergens must not be recommended", "containsUndeclaredAllergen(y)", "prohibition"),
    ("Products with declared allergens may be recommended only when safe for the user", "hasAllergenLabel(y)∧safeFor(x,y)", "permission"),
    ("Products with missing allergen labels must not be recommended to allergic users", "allergicTo(x,Nuts)∧¬hasAllergenLabel(y)", "prohibition"),
    ("Products containing nuts must include allergen labeling for allergic users", "allergicTo(x,Nuts)∧contains(y,Nuts)∧hasAllergenLabel(y)", "obligation"),
    ("Products containing shellfish must include allergen labeling for allergic users", "allergicTo(x,Shellfish)∧contains(y,Shellfish)∧hasAllergenLabel(y)", "obligation"),
    ("Users requiring halal food may receive verified halal products", "requiresHalal(x)∧verifiedHalal(y)", "permission"),
    ("Users requiring halal food must not receive non halal products", "requiresHalal(x)∧nonHalal(y)", "prohibition"),
    ("Users requiring halal food must receive products with verified halal status", "requiresHalal(x)∧halalMeal(y)∧verifiedHalal(y)", "obligation"),
    ("Users requiring halal food must not receive products with uncertain halal status", "requiresHalal(x)∧uncertainHalalStatus(y)", "prohibition"),
    ("Verified halal products may be recommended when labeling is compliant", "verifiedHalal(y)∧compliesWithLabeling(y)", "permission"),
    ("Users requiring kosher food may receive verified kosher products", "requiresKosher(x)∧verifiedKosher(y)", "permission"),
    ("Users requiring kosher food must not receive non kosher products", "requiresKosher(x)∧nonKosher(y)", "prohibition"),
    ("Users requiring kosher food must receive products with verified kosher status", "requiresKosher(x)∧kosherMeal(y)∧verifiedKosher(y)", "obligation"),
    ("Users requiring kosher food must not receive products with uncertain kosher status", "requiresKosher(x)∧uncertainKosherStatus(y)", "prohibition"),
    ("Verified kosher products may be recommended when labeling is compliant", "verifiedKosher(y)∧compliesWithLabeling(y)", "permission"),
    ("Gluten sensitive users must receive certified gluten free products", "glutenSensitive(x)∧certifiedGlutenFree(y)", "obligation"),
    ("Users requiring gluten free food must not receive products containing gluten", "requiresGlutenFree(x)∧contains(y,Gluten)", "prohibition"),
    ("Users requiring gluten free food may receive certified gluten free products", "requiresGlutenFree(x)∧certifiedGlutenFree(y)", "permission"),
    ("Gluten sensitive users must not receive uncertified gluten free claims", "glutenSensitive(x)∧misleadingClaim(y)", "prohibition"),
    ("Certified gluten free products must comply with labeling rules", "certifiedGlutenFree(y)∧compliesWithLabeling(y)", "obligation"),
    ("Lactose intolerant users must receive certified lactose free products", "lactoseIntolerant(x)∧certifiedLactoseFree(y)", "obligation"),
    ("Users requiring lactose free food must not receive products containing lactose", "requiresLactoseFree(x)∧contains(y,Lactose)", "prohibition"),
    ("Users requiring lactose free food may receive certified lactose free products", "requiresLactoseFree(x)∧certifiedLactoseFree(y)", "permission"),
    ("Lactose intolerant users must not receive misleading lactose free claims", "lactoseIntolerant(x)∧misleadingClaim(y)", "prohibition"),
    ("Certified lactose free products must comply with labeling rules", "certifiedLactoseFree(y)∧compliesWithLabeling(y)", "obligation"),
    ("Foods approved by the ministry may be recommended", "approvedByMinistry(y)", "permission"),
    ("Restricted foods must not be recommended", "restricted(y)", "prohibition"),
    ("Foods complying with ministry guidelines should be recommended when suitable", "compliesWithGuideline(y)∧safeFor(x,y)", "obligation"),
    ("Foods without nutrition labels must not be recommended as approved foods", "approvedByMinistry(y)∧¬hasNutritionLabel(y)", "prohibition"),
    ("Foods with nutrition labels may be recommended to adults", "adult(x)∧hasNutritionLabel(y)", "permission"),
    ("Products exceeding fat limits must not be recommended to vulnerable users", "vulnerableUser(x)∧exceedsFatLimit(y)", "prohibition"),
    ("Vulnerable users must receive foods complying with ministry guidelines", "vulnerableUser(x)∧compliesWithGuideline(y)", "obligation"),
    ("Vulnerable users may receive approved healthy meals", "vulnerableUser(x)∧approvedByMinistry(y)∧healthyMeal(y)", "permission"),
    ("Vulnerable users must not receive unsafe products", "vulnerableUser(x)∧unsafeProduct(y)", "prohibition"),
    ("Vulnerable users must receive affordable healthy meal options", "vulnerableUser(x)∧affordableMeal(y)∧healthyMeal(y)", "obligation"),
    ("Energy drinks requiring warnings must not be recommended to children", "child(x)∧energyDrink(y)∧requiresWarning(y)", "prohibition"),
    ("Products requiring safety warnings must include warning labels", "requiresWarning(y)∧hasSafetyWarning(y)", "obligation"),
    ("Products without required safety warnings must not be recommended", "requiresWarning(y)∧¬hasSafetyWarning(y)", "prohibition"),
    ("Adults may receive products with safety warnings when warnings are shown", "adult(x)∧hasSafetyWarning(y)", "permission"),
    ("Warning products must not be recommended to vulnerable users", "vulnerableUser(x)∧safetyWarningProduct(y)", "prohibition"),
    ("Organic products with misleading claims must not be recommended", "organicFood(y)∧misleadingClaim(y)", "prohibition"),
    ("Sustainable products with misleading claims must not be recommended", "sustainable(y)∧misleadingClaim(y)", "prohibition"),
    ("Products with verified organic claims may be recommended", "organicFood(y)∧verifiedClaim(y)", "permission"),
    ("Products with verified sustainability claims may be recommended", "sustainable(y)∧verifiedClaim(y)", "permission"),
    ("Products with misleading nutrition claims must not be recommended", "nutritionClaim(y)∧misleadingClaim(y)", "prohibition"),
    ("Affordable healthy foods should be recommended to children", "child(x)∧affordableMeal(y)∧healthyMeal(y)", "obligation"),
    ("Affordable ministry approved healthy foods should be recommended to vulnerable users", "vulnerableUser(x)∧affordableMeal(y)∧healthyMeal(y)∧approvedByMinistry(y)", "obligation"),
    ("Affordable approved foods may be recommended to adults", "adult(x)∧affordableMeal(y)∧approvedByMinistry(y)", "permission"),
    ("Unaffordable essential foods should not be the only recommended option", "essentialFood(y)∧unaffordable(y)", "prohibition"),
    ("Healthy affordable alternatives should be recommended when restricted foods are present", "healthyMeal(y)∧affordableMeal(y)∧alternativeToRestrictedFood(y)", "obligation"),
    ("Products banned for children must not be recommended to children", "child(x)∧bannedForChildren(y)", "prohibition"),
    ("Products with age restrictions may be recommended to adults", "adult(x)∧ageRestrictedProduct(y)", "permission"),
    ("Age restricted products must not be recommended to underage users", "underage(x)∧ageRestrictedProduct(y)", "prohibition"),
    ("Products suitable for children should be recommended to children when healthy", "child(x)∧suitableForChildren(y)∧healthyMeal(y)", "obligation"),
    ("Products unsuitable for children must not be recommended to children", "child(x)∧unsuitableForChildren(y)", "prohibition"),
    ("High sugar products must not be recommended to users with low sugar requirements", "requiresLowSugar(x)∧highSugarProduct(y)", "prohibition"),
    ("Low sugar products should be recommended to users with low sugar requirements", "requiresLowSugar(x)∧lowSugarFood(y)", "obligation"),
    ("High salt products must not be recommended to users with low salt requirements", "requiresLowSalt(x)∧highSaltProduct(y)", "prohibition"),
    ("Low salt products should be recommended to users with low salt requirements", "requiresLowSalt(x)∧lowSaltFood(y)", "obligation"),
    ("Low fat products may be recommended to users avoiding high fat products", "avoids(x,y)∧lowFatMeal(y)", "permission"),
    ("Products containing undeclared allergens must be treated as unsafe products", "containsUndeclaredAllergen(y)∧unsafeProduct(y)", "prohibition"),
    ("Unsafe products must not be recommended to any user", "unsafeProduct(y)", "prohibition"),
    ("Safe products may be recommended when suitable for the user", "safeFor(x,y)", "permission"),
    ("Products approved by the ministry and safe for the user should be recommended", "approvedByMinistry(y)∧safeFor(x,y)", "obligation"),
    ("Products restricted by the ministry must not be recommended even if preferred", "restricted(y)∧prefers(x,y)", "prohibition"),
    ("Foods lacking required certification must not be recommended to users requiring certification", "requiresCertifiedProduct(x)∧¬certified(y)", "prohibition"),
    ("Certified foods may be recommended to users requiring certified products", "requiresCertifiedProduct(x)∧certified(y)", "permission"),
    ("Products with complete labels should be recommended over products with incomplete labels", "completeLabel(y)∧compliesWithLabeling(y)", "obligation"),
    ("Products with incomplete labels must not be recommended to vulnerable users", "vulnerableUser(x)∧incompleteLabel(y)", "prohibition"),
    ("Products failing nutrition guidelines must not be recommended to vulnerable users", "vulnerableUser(x)∧¬meetsNutritionGuideline(y)", "prohibition"),
]


def formula(condition, norm_type, dyadic=False):
    modal = MODAL[norm_type]
    action = "recommend(System,y,x)"
    if dyadic:
        return f"∀x.∀y.{modal}({action}|{condition})"
    return f"∀x.∀y.{condition}->{modal}({action})"


def regulatory_text(nl_norm, norm_type):
    if norm_type == "prohibition":
        return f"Food Ministry regulation prohibits the recommender from violating this safety rule: {nl_norm}."
    if norm_type == "obligation":
        return f"Food Ministry policy requires the recommender to follow this public-interest rule: {nl_norm}."
    if norm_type == "permission":
        return f"Food Ministry policy permits the recommender to act under this regulatory condition: {nl_norm}."
    return nl_norm


def main():
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "stakeholder", "nl_norm", "implication_formula", "dyadic_formula", "norm_type"])
        for index, (nl_norm, condition, norm_type) in enumerate(ROWS, start=1):
            writer.writerow([
                f"MINISTRY{index:03d}",
                "Food Ministry",
                regulatory_text(nl_norm, norm_type),
                formula(condition, norm_type, dyadic=False),
                formula(condition, norm_type, dyadic=True),
                norm_type,
            ])


if __name__ == "__main__":
    main()
