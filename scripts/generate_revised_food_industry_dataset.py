import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT = PROJECT_ROOT / "data" / "revised" / "food_industry_dataset.csv"

MODAL = {
    "obligation": "O",
    "permission": "P",
    "prohibition": "F",
}


ROWS = [
    ("Eligible users should receive sponsored product recommendations when products are available", "eligible(x)∧sponsored(y)∧available(y)", "obligation"),
    ("Eligible adults may receive sponsored product recommendations", "eligible(x)∧adult(x)∧sponsored(y)", "permission"),
    ("Ineligible users should not receive sponsored product recommendations", "¬eligible(x)∧sponsored(y)", "prohibition"),
    ("Sponsored products should be recommended when they are approved and available", "sponsored(y)∧approved(y)∧available(y)", "obligation"),
    ("Sponsored products should not be recommended when they are restricted", "sponsored(y)∧restricted(y)", "prohibition"),
    ("Loyal customers may receive premium product recommendations", "loyalCustomer(x)∧premiumProduct(y)", "permission"),
    ("Premium customers should receive premium product recommendations when products are available", "premiumCustomer(x)∧premiumProduct(y)∧available(y)", "obligation"),
    ("Children should not receive restricted premium product promotions", "child(x)∧premiumProduct(y)∧restricted(y)", "prohibition"),
    ("Premium products may be recommended when they are approved", "premiumProduct(y)∧approved(y)", "permission"),
    ("Premium products should be recommended to eligible premium customers", "eligible(x)∧premiumCustomer(x)∧premiumProduct(y)", "obligation"),
    ("Certified products should be recommended to users requiring certified products", "requiresCertifiedProduct(x)∧certified(y)", "obligation"),
    ("Certified products may be promoted when they are available", "certified(y)∧available(y)", "permission"),
    ("Uncertified products should not be recommended to users requiring certified products", "requiresCertifiedProduct(x)∧¬certified(y)", "prohibition"),
    ("Certified healthy products should be recommended to eligible users", "eligible(x)∧certified(y)∧healthyMeal(y)", "obligation"),
    ("Certified products should not be recommended when they are restricted", "certified(y)∧restricted(y)", "prohibition"),
    ("Users interested in discounted food should receive discounted product recommendations", "interestedIn(x,DiscountedFood)∧discounted(y)", "obligation"),
    ("Loyal customers may receive discounted seasonal products", "loyalCustomer(x)∧discounted(y)∧seasonal(y)", "permission"),
    ("Users avoiding discounted products should not receive discounted product recommendations", "avoids(x,y)∧discounted(y)", "prohibition"),
    ("Discounted products should be recommended when they are available", "discounted(y)∧available(y)", "obligation"),
    ("Discounted products may be recommended to eligible adults", "eligible(x)∧adult(x)∧discounted(y)", "permission"),
    ("Seasonal products should be recommended during seasonal campaigns", "seasonal(y)∧available(y)", "obligation"),
    ("Users interested in seasonal food may receive seasonal product recommendations", "interestedIn(x,SeasonalFood)∧seasonal(y)", "permission"),
    ("Seasonal products should not be recommended when unavailable", "seasonal(y)∧¬available(y)", "prohibition"),
    ("Loyal customers should receive available seasonal product recommendations", "loyalCustomer(x)∧seasonal(y)∧available(y)", "obligation"),
    ("Seasonal products may be recommended to adults when approved", "adult(x)∧seasonal(y)∧approved(y)", "permission"),
    ("Users interested in new products should receive new product recommendations", "interestedIn(x,NewProduct)∧newProduct(y)", "obligation"),
    ("New products may be recommended to eligible users", "eligible(x)∧newProduct(y)", "permission"),
    ("New products should not be recommended when restricted", "newProduct(y)∧restricted(y)", "prohibition"),
    ("New approved products should be promoted to adults", "adult(x)∧newProduct(y)∧approved(y)", "obligation"),
    ("New products may be recommended when they are available", "newProduct(y)∧available(y)", "permission"),
    ("Users interested in local food should receive local product recommendations", "interestedIn(x,LocalFood)∧localProduct(y)", "obligation"),
    ("Local products may be recommended when available", "localProduct(y)∧available(y)", "permission"),
    ("Unavailable local products should not be recommended", "localProduct(y)∧¬available(y)", "prohibition"),
    ("Local sustainable products should be recommended to users interested in local food", "interestedIn(x,LocalFood)∧localProduct(y)∧sustainable(y)", "obligation"),
    ("Local products may be recommended to loyal customers", "loyalCustomer(x)∧localProduct(y)", "permission"),
    ("Users interested in sustainable food should receive sustainable product recommendations", "interestedIn(x,SustainableFood)∧sustainable(y)", "obligation"),
    ("Sustainable products may be recommended when available", "sustainable(y)∧available(y)", "permission"),
    ("Sustainable products should not be recommended when sustainability claims are misleading", "sustainable(y)∧misleadingClaim(y)", "prohibition"),
    ("Certified sustainable products should be recommended to eligible users", "eligible(x)∧sustainable(y)∧certified(y)", "obligation"),
    ("Sustainable products may be recommended to premium customers", "premiumCustomer(x)∧sustainable(y)", "permission"),
    ("Organic products should be recommended to users preferring organic products", "prefers(x,y)∧organic(y)", "obligation"),
    ("Organic products may be recommended when verified", "organic(y)∧verifiedClaim(y)", "permission"),
    ("Organic products should not be recommended when organic claims are misleading", "organic(y)∧misleadingClaim(y)", "prohibition"),
    ("Certified organic products should be promoted to eligible users", "eligible(x)∧organic(y)∧certified(y)", "obligation"),
    ("Organic products may be recommended to loyal customers", "loyalCustomer(x)∧organic(y)", "permission"),
    ("Affordable products should be recommended to users preferring affordable meals", "prefers(x,y)∧affordable(y)", "obligation"),
    ("Affordable products may be recommended when available", "affordable(y)∧available(y)", "permission"),
    ("Unaffordable products should not be recommended to users preferring affordable meals", "prefers(x,y)∧unaffordable(y)", "prohibition"),
    ("Affordable sponsored products should be recommended to eligible users", "eligible(x)∧affordable(y)∧sponsored(y)", "obligation"),
    ("Affordable products may be recommended to adults", "adult(x)∧affordable(y)", "permission"),
    ("Users requiring halal food should receive certified halal product recommendations", "requiresHalal(x)∧certifiedHalal(y)", "obligation"),
    ("Halal certified products may be recommended to users requiring halal food", "requiresHalal(x)∧certifiedHalal(y)∧available(y)", "permission"),
    ("Products without halal certification should not be recommended to users requiring halal food", "requiresHalal(x)∧¬certifiedHalal(y)", "prohibition"),
    ("Halal certified sponsored products should be promoted to eligible halal users", "eligible(x)∧requiresHalal(x)∧certifiedHalal(y)∧sponsored(y)", "obligation"),
    ("Halal certified products may be recommended when approved", "certifiedHalal(y)∧approved(y)", "permission"),
    ("Users requiring kosher food should receive certified kosher product recommendations", "requiresKosher(x)∧certifiedKosher(y)", "obligation"),
    ("Kosher certified products may be recommended to users requiring kosher food", "requiresKosher(x)∧certifiedKosher(y)∧available(y)", "permission"),
    ("Products without kosher certification should not be recommended to users requiring kosher food", "requiresKosher(x)∧¬certifiedKosher(y)", "prohibition"),
    ("Kosher certified sponsored products should be promoted to eligible kosher users", "eligible(x)∧requiresKosher(x)∧certifiedKosher(y)∧sponsored(y)", "obligation"),
    ("Kosher certified products may be recommended when approved", "certifiedKosher(y)∧approved(y)", "permission"),
    ("Users requiring gluten free food should receive certified gluten free product recommendations", "requiresGlutenFree(x)∧certifiedGlutenFree(y)", "obligation"),
    ("Certified gluten free products may be recommended to gluten sensitive users", "glutenSensitive(x)∧certifiedGlutenFree(y)", "permission"),
    ("Products without gluten free certification should not be recommended to gluten sensitive users", "glutenSensitive(x)∧¬certifiedGlutenFree(y)", "prohibition"),
    ("Certified gluten free sponsored products should be promoted to eligible gluten free users", "eligible(x)∧requiresGlutenFree(x)∧certifiedGlutenFree(y)∧sponsored(y)", "obligation"),
    ("Certified gluten free products may be recommended when available", "certifiedGlutenFree(y)∧available(y)", "permission"),
    ("Users requiring lactose free food should receive certified lactose free product recommendations", "requiresLactoseFree(x)∧certifiedLactoseFree(y)", "obligation"),
    ("Certified lactose free products may be recommended to lactose intolerant users", "lactoseIntolerant(x)∧certifiedLactoseFree(y)", "permission"),
    ("Products without lactose free certification should not be recommended to lactose intolerant users", "lactoseIntolerant(x)∧¬certifiedLactoseFree(y)", "prohibition"),
    ("Certified lactose free sponsored products should be promoted to eligible lactose free users", "eligible(x)∧requiresLactoseFree(x)∧certifiedLactoseFree(y)∧sponsored(y)", "obligation"),
    ("Certified lactose free products may be recommended when available", "certifiedLactoseFree(y)∧available(y)", "permission"),
    ("Users interested in Mediterranean products should receive Mediterranean meal recommendations", "interestedIn(x,Mediterranean)∧mediterraneanMeal(y)", "obligation"),
    ("Mediterranean meals may be recommended when available", "mediterraneanMeal(y)∧available(y)", "permission"),
    ("Mediterranean sponsored meals should not be recommended when restricted", "mediterraneanMeal(y)∧sponsored(y)∧restricted(y)", "prohibition"),
    ("Certified Mediterranean meals should be promoted to eligible users", "eligible(x)∧mediterraneanMeal(y)∧certified(y)", "obligation"),
    ("Mediterranean meals may be recommended to loyal customers", "loyalCustomer(x)∧mediterraneanMeal(y)", "permission"),
    ("Users interested in Asian products should receive Asian meal recommendations", "interestedIn(x,Asian)∧asianMeal(y)", "obligation"),
    ("Asian meals may be recommended when available", "asianMeal(y)∧available(y)", "permission"),
    ("Asian sponsored meals should not be recommended when restricted", "asianMeal(y)∧sponsored(y)∧restricted(y)", "prohibition"),
    ("Certified Asian meals should be promoted to eligible users", "eligible(x)∧asianMeal(y)∧certified(y)", "obligation"),
    ("Asian meals may be recommended to loyal customers", "loyalCustomer(x)∧asianMeal(y)", "permission"),
    ("Users preferring spicy products may receive spicy meal recommendations", "prefers(x,y)∧spicy(y)", "permission"),
    ("Spicy products should be promoted to users interested in spicy products", "interestedIn(x,SpicyFood)∧spicy(y)", "obligation"),
    ("Spicy products should not be recommended to users avoiding spicy products", "avoids(x,y)∧spicy(y)", "prohibition"),
    ("Mild products may be recommended to users avoiding spicy products", "avoids(x,y)∧mild(y)", "permission"),
    ("Mild products should be recommended to users preferring mild meals", "prefers(x,y)∧mild(y)", "obligation"),
    ("Products unsafe for a user should not be recommended", "¬safeFor(x,y)", "prohibition"),
    ("Products containing nuts should not be recommended to nut allergic users", "allergicTo(x,Nuts)∧contains(y,Nuts)", "prohibition"),
    ("Products containing shellfish should not be recommended to shellfish allergic users", "allergicTo(x,Shellfish)∧contains(y,Shellfish)", "prohibition"),
    ("Approved products may be recommended to eligible users", "eligible(x)∧approved(y)", "permission"),
    ("Approved sponsored products should be promoted to eligible users", "eligible(x)∧approved(y)∧sponsored(y)", "obligation"),
    ("Unavailable products should not be recommended", "¬available(y)", "prohibition"),
    ("Available approved products may be recommended to adults", "adult(x)∧available(y)∧approved(y)", "permission"),
    ("Available certified products should be recommended to loyal customers", "loyalCustomer(x)∧available(y)∧certified(y)", "obligation"),
    ("Restricted products should not be recommended even when sponsored", "restricted(y)∧sponsored(y)", "prohibition"),
    ("Brand safe products may be recommended to eligible users", "eligible(x)∧brandSafe(y)", "permission"),
    ("Brand unsafe products should not be recommended", "brandUnsafe(y)", "prohibition"),
    ("Market preference products should be promoted to interested users", "interestedIn(x,MarketPreference)∧marketPreferenceProduct(y)", "obligation"),
    ("Cuisine specific products may be recommended to interested users", "interestedIn(x,CuisineSpecific)∧cuisineSpecificProduct(y)", "permission"),
    ("Sponsored products conflicting with user safety should not be recommended", "sponsored(y)∧¬safeFor(x,y)", "prohibition"),
    ("Available brand safe sponsored products should be recommended to loyal eligible users", "eligible(x)∧loyalCustomer(x)∧sponsored(y)∧available(y)∧brandSafe(y)", "obligation"),
]


def formula(condition, norm_type, dyadic=False):
    modal = MODAL[norm_type]
    action = "recommend(System,y,x)"
    if dyadic:
        return f"∀x.∀y.{modal}({action}|{condition})"
    return f"∀x.∀y.{condition}->{modal}({action})"


def industry_text(nl_norm, norm_type):
    if norm_type == "obligation":
        return f"Food Industry policy requires the recommender to support this commercial objective: {nl_norm}."
    if norm_type == "permission":
        return f"Food Industry policy permits the recommender to use this market placement rule: {nl_norm}."
    if norm_type == "prohibition":
        return f"Food Industry compliance prohibits the recommender from violating this product-suitability rule: {nl_norm}."
    return nl_norm


def main():
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "stakeholder", "nl_norm", "implication_formula", "dyadic_formula", "norm_type"])
        for index, (nl_norm, condition, norm_type) in enumerate(ROWS, start=1):
            writer.writerow([
                f"INDUSTRY{index:03d}",
                "Food Industry",
                industry_text(nl_norm, norm_type),
                formula(condition, norm_type, dyadic=False),
                formula(condition, norm_type, dyadic=True),
                norm_type,
            ])


if __name__ == "__main__":
    main()
