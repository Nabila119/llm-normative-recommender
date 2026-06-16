import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT = PROJECT_ROOT / "data" / "revised" / "constitutive_rules.csv"


ROWS = [
    ("Shellfish meals count as non-vegan products", "shellfishMeal(y)->nonVegan(y)", "dietaryClassification"),
    ("Meat meals count as non-vegan products", "meatMeal(y)->nonVegan(y)", "dietaryClassification"),
    ("Dairy meals count as non-vegan products", "dairyMeal(y)->nonVegan(y)", "dietaryClassification"),
    ("Egg meals count as non-vegan products", "eggMeal(y)->nonVegan(y)", "dietaryClassification"),
    ("Honey products count as non-vegan products", "honeyProduct(y)->nonVegan(y)", "dietaryClassification"),
    ("Meat meals count as non-vegetarian products", "meatMeal(y)->nonVegetarian(y)", "dietaryClassification"),
    ("Shellfish meals count as non-vegetarian products", "shellfishMeal(y)->nonVegetarian(y)", "dietaryClassification"),
    ("Fish meals count as non-vegetarian products", "fishMeal(y)->nonVegetarian(y)", "dietaryClassification"),
    ("Chicken meals count as non-vegetarian products", "chickenMeal(y)->nonVegetarian(y)", "dietaryClassification"),
    ("Beef meals count as non-vegetarian products", "beefMeal(y)->nonVegetarian(y)", "dietaryClassification"),
    ("Energy drinks count as high sugar products", "energyDrink(y)->highSugarProduct(y)", "nutritionClassification"),
    ("Sugary snacks count as high sugar products", "sugarySnack(y)->highSugarProduct(y)", "nutritionClassification"),
    ("Candy products count as high sugar products", "candyProduct(y)->highSugarProduct(y)", "nutritionClassification"),
    ("Sweet desserts count as high sugar products", "sweetDessert(y)->highSugarProduct(y)", "nutritionClassification"),
    ("Regular soda counts as a high sugar product", "regularSoda(y)->highSugarProduct(y)", "nutritionClassification"),
    ("Salty snacks count as high salt products", "saltySnack(y)->highSaltProduct(y)", "nutritionClassification"),
    ("Processed meat counts as a high salt product", "processedMeat(y)->highSaltProduct(y)", "nutritionClassification"),
    ("Instant noodles count as high salt products", "instantNoodles(y)->highSaltProduct(y)", "nutritionClassification"),
    ("Salted nuts count as high salt products", "saltedNuts(y)->highSaltProduct(y)", "nutritionClassification"),
    ("Canned soup counts as a high salt product", "cannedSoup(y)->highSaltProduct(y)", "nutritionClassification"),
    ("Fried meals count as high fat products", "friedMeal(y)->highFatProduct(y)", "nutritionClassification"),
    ("Cream desserts count as high fat products", "creamDessert(y)->highFatProduct(y)", "nutritionClassification"),
    ("Fast food meals count as high fat products", "fastFoodMeal(y)->highFatProduct(y)", "nutritionClassification"),
    ("Cheese meals count as high fat products", "cheeseMeal(y)->highFatProduct(y)", "nutritionClassification"),
    ("Butter products count as high fat products", "butterProduct(y)->highFatProduct(y)", "nutritionClassification"),
    ("Nut snacks contain nuts", "nutSnack(y)->contains(y,Nuts)", "allergenClassification"),
    ("Peanut snacks contain nuts", "peanutSnack(y)->contains(y,Nuts)", "allergenClassification"),
    ("Almond desserts contain nuts", "almondDessert(y)->contains(y,Nuts)", "allergenClassification"),
    ("Shellfish meals contain shellfish", "shellfishMeal(y)->contains(y,Shellfish)", "allergenClassification"),
    ("Shrimp meals contain shellfish", "shrimpMeal(y)->contains(y,Shellfish)", "allergenClassification"),
    ("Wheat meals contain gluten", "wheatMeal(y)->contains(y,Gluten)", "medicalSuitability"),
    ("Bread products contain gluten", "breadProduct(y)->contains(y,Gluten)", "medicalSuitability"),
    ("Regular pasta contains gluten", "regularPasta(y)->contains(y,Gluten)", "medicalSuitability"),
    ("Dairy meals contain lactose", "dairyMeal(y)->contains(y,Lactose)", "medicalSuitability"),
    ("Milk products contain lactose", "milkProduct(y)->contains(y,Lactose)", "medicalSuitability"),
    ("Cheese meals contain lactose", "cheeseMeal(y)->contains(y,Lactose)", "medicalSuitability"),
    ("Pork meals count as non-halal products", "porkMeal(y)->nonHalal(y)", "religiousClassification"),
    ("Alcohol products count as non-halal products", "alcoholProduct(y)->nonHalal(y)", "religiousClassification"),
    ("Non certified meat counts as uncertain halal status", "nonCertifiedMeat(y)->uncertainHalalStatus(y)", "religiousClassification"),
    ("Pork meals count as non-kosher products", "porkMeal(y)->nonKosher(y)", "religiousClassification"),
    ("Shellfish meals count as non-kosher products", "shellfishMeal(y)->nonKosher(y)", "religiousClassification"),
    ("Non certified meat counts as uncertain kosher status", "nonCertifiedMeat(y)->uncertainKosherStatus(y)", "religiousClassification"),
    ("Energy drinks count as age restricted products", "energyDrink(y)->ageRestrictedProduct(y)", "productSafety"),
    ("Products requiring warnings count as safety warning products", "requiresWarning(y)->safetyWarningProduct(y)", "productSafety"),
    ("Products containing undeclared allergens count as unsafe products", "containsUndeclaredAllergen(y)->unsafeProduct(y)", "productSafety"),
    ("Organic foods count as market preference products", "organicFood(y)->marketPreferenceProduct(y)", "marketClassification"),
    ("Sustainable meals count as market preference products", "sustainable(y)->marketPreferenceProduct(y)", "marketClassification"),
    ("Seasonal meals count as market preference products", "seasonalMeal(y)->marketPreferenceProduct(y)", "marketClassification"),
    ("Mediterranean meals count as cuisine specific products", "mediterraneanMeal(y)->cuisineSpecificProduct(y)", "marketClassification"),
    ("Asian meals count as cuisine specific products", "asianMeal(y)->cuisineSpecificProduct(y)", "marketClassification"),
]


def main():
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "scope", "nl_rule", "logic_rule", "category"])
        for index, (nl_rule, body, category) in enumerate(ROWS, start=1):
            writer.writerow([
                f"CR{index:03d}",
                "FoodDomain",
                nl_rule,
                f"∀y.{body}",
                category,
            ])


if __name__ == "__main__":
    main()
