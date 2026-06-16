import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUT = PROJECT_ROOT / "data" / "revised" / "user_dataset.csv"

MODAL = {
    "obligation": "O",
    "permission": "P",
    "prohibition": "F",
}


ROWS = [
    ("Children should not receive energy drink recommendations", "child(x)∧energyDrink(y)", "prohibition"),
    ("Children should not receive high sugar product recommendations", "child(x)∧highSugarProduct(y)", "prohibition"),
    ("Children should receive healthy meal recommendations", "child(x)∧healthyMeal(y)", "obligation"),
    ("Children may receive mild meal recommendations", "child(x)∧mildMeal(y)", "permission"),
    ("Children should not receive ultra processed food recommendations", "child(x)∧ultraProcessedFood(y)", "prohibition"),
    ("Diabetic users should receive low sugar food recommendations", "diabetic(x)∧lowSugarFood(y)", "obligation"),
    ("Diabetic users should not receive sugary snack recommendations", "diabetic(x)∧sugarySnack(y)", "prohibition"),
    ("Diabetic users may receive certified healthy meal recommendations", "diabetic(x)∧healthyMeal(y)∧certifiedHealthy(y)", "permission"),
    ("Diabetic users should not receive energy drinks that are high sugar products", "diabetic(x)∧energyDrink(y)∧highSugarProduct(y)", "prohibition"),
    ("Diabetic users should receive affordable low sugar food recommendations", "diabetic(x)∧lowSugarFood(y)∧affordableMeal(y)", "obligation"),
    ("Hypertensive users should receive low salt food recommendations", "hypertensive(x)∧lowSaltFood(y)", "obligation"),
    ("Hypertensive users should not receive salty snack recommendations", "hypertensive(x)∧saltySnack(y)", "prohibition"),
    ("Hypertensive users may receive healthy low salt meal recommendations", "hypertensive(x)∧healthyMeal(y)∧lowSaltFood(y)", "permission"),
    ("Users requiring low salt food should not receive high salt products", "requiresLowSalt(x)∧highSaltProduct(y)", "prohibition"),
    ("Users requiring low salt food should receive low salt alternatives", "requiresLowSalt(x)∧lowSaltFood(y)", "obligation"),
    ("Pregnant users should receive safe meal recommendations", "pregnant(x)∧safeForPregnantUsers(y)", "obligation"),
    ("Pregnant users should not receive energy drink recommendations", "pregnant(x)∧energyDrink(y)", "prohibition"),
    ("Pregnant users may receive mild healthy meal recommendations", "pregnant(x)∧mildMeal(y)∧healthyMeal(y)", "permission"),
    ("Pregnant users should not receive products requiring safety warnings", "pregnant(x)∧requiresWarning(y)", "prohibition"),
    ("Pregnant users should receive affordable healthy meal recommendations", "pregnant(x)∧healthyMeal(y)∧affordableMeal(y)", "obligation"),
    ("Elderly users should receive healthy meal recommendations", "elderly(x)∧healthyMeal(y)", "obligation"),
    ("Elderly users should not receive high salt product recommendations", "elderly(x)∧highSaltProduct(y)", "prohibition"),
    ("Elderly users may receive low sugar food recommendations", "elderly(x)∧lowSugarFood(y)", "permission"),
    ("Elderly users should receive affordable meal recommendations", "elderly(x)∧affordableMeal(y)", "obligation"),
    ("Elderly users should not receive ultra processed food recommendations", "elderly(x)∧ultraProcessedFood(y)", "prohibition"),
    ("Users allergic to nuts should not receive products containing nuts", "allergicTo(x,Nuts)∧contains(y,Nuts)", "prohibition"),
    ("Users allergic to shellfish should not receive products containing shellfish", "allergicTo(x,Shellfish)∧contains(y,Shellfish)", "prohibition"),
    ("Users allergic to nuts should receive nut free meal recommendations", "allergicTo(x,Nuts)∧nutFreeMeal(y)", "obligation"),
    ("Users allergic to shellfish may receive shellfish free meal recommendations", "allergicTo(x,Shellfish)∧shellfishFreeMeal(y)", "permission"),
    ("Users allergic to nuts or shellfish should receive allergen safe meal recommendations", "allergicTo(x,Nuts)∨allergicTo(x,Shellfish)∧allergenSafeMeal(y)", "obligation"),
    ("Vegan users should not receive non vegan meal recommendations", "vegan(x)∧nonVegan(y)", "prohibition"),
    ("Vegan users should receive vegan meal recommendations", "vegan(x)∧veganMeal(y)", "obligation"),
    ("Vegan users may receive plant based meal recommendations", "vegan(x)∧plantBasedMeal(y)", "permission"),
    ("Vegan users should not receive dairy meal recommendations", "vegan(x)∧dairyMeal(y)", "prohibition"),
    ("Vegan users should receive sustainable vegan meal recommendations", "vegan(x)∧veganMeal(y)∧sustainable(y)", "obligation"),
    ("Vegetarian users should not receive meat meal recommendations", "vegetarian(x)∧meatMeal(y)", "prohibition"),
    ("Vegetarian users should receive vegetarian meal recommendations", "vegetarian(x)∧vegetarianMeal(y)", "obligation"),
    ("Vegetarian users may receive plant based meal recommendations", "vegetarian(x)∧plantBasedMeal(y)", "permission"),
    ("Vegetarian users should not receive non vegetarian products", "vegetarian(x)∧nonVegetarian(y)", "prohibition"),
    ("Vegetarian users should receive affordable vegetarian meals", "vegetarian(x)∧vegetarianMeal(y)∧affordableMeal(y)", "obligation"),
    ("Users requiring halal food should receive certified halal meal recommendations", "requiresHalal(x)∧halalMeal(y)∧certifiedHalal(y)", "obligation"),
    ("Users requiring halal food should not receive non halal meal recommendations", "requiresHalal(x)∧nonHalal(y)", "prohibition"),
    ("Users requiring halal food may receive verified halal products", "requiresHalal(x)∧verifiedHalal(y)", "permission"),
    ("Users requiring halal food should not receive products with uncertain halal status", "requiresHalal(x)∧uncertainHalalStatus(y)", "prohibition"),
    ("Users preferring halal food may receive halal meal recommendations", "prefers(x,y)∧halalMeal(y)", "permission"),
    ("Users requiring kosher food should receive certified kosher meal recommendations", "requiresKosher(x)∧kosherMeal(y)∧certifiedKosher(y)", "obligation"),
    ("Users requiring kosher food should not receive non kosher meal recommendations", "requiresKosher(x)∧nonKosher(y)", "prohibition"),
    ("Users requiring kosher food may receive verified kosher products", "requiresKosher(x)∧verifiedKosher(y)", "permission"),
    ("Users requiring kosher food should not receive products with uncertain kosher status", "requiresKosher(x)∧uncertainKosherStatus(y)", "prohibition"),
    ("Users preferring kosher food may receive kosher meal recommendations", "prefers(x,y)∧kosherMeal(y)", "permission"),
    ("Gluten sensitive users should receive certified gluten free meal recommendations", "glutenSensitive(x)∧glutenFreeMeal(y)∧certifiedGlutenFree(y)", "obligation"),
    ("Users requiring gluten free food should not receive gluten containing products", "requiresGlutenFree(x)∧contains(y,Gluten)", "prohibition"),
    ("Users requiring gluten free food may receive certified gluten free products", "requiresGlutenFree(x)∧certifiedGlutenFree(y)", "permission"),
    ("Gluten sensitive users should not receive wheat meal recommendations", "glutenSensitive(x)∧wheatMeal(y)", "prohibition"),
    ("Users requiring gluten free food should receive gluten free meal recommendations", "requiresGlutenFree(x)∧glutenFreeMeal(y)", "obligation"),
    ("Lactose intolerant users should receive certified lactose free meal recommendations", "lactoseIntolerant(x)∧lactoseFreeMeal(y)∧certifiedLactoseFree(y)", "obligation"),
    ("Users requiring lactose free food should not receive dairy meal recommendations", "requiresLactoseFree(x)∧dairyMeal(y)", "prohibition"),
    ("Users requiring lactose free food may receive lactose free products", "requiresLactoseFree(x)∧lactoseFreeMeal(y)", "permission"),
    ("Lactose intolerant users should not receive products containing lactose", "lactoseIntolerant(x)∧contains(y,Lactose)", "prohibition"),
    ("Users requiring lactose free food should receive certified lactose free products", "requiresLactoseFree(x)∧certifiedLactoseFree(y)", "obligation"),
    ("Users preferring organic food should receive organic food recommendations", "prefers(x,y)∧organicFood(y)", "obligation"),
    ("Users preferring sustainable food should receive sustainable meal recommendations", "prefers(x,y)∧sustainable(y)", "obligation"),
    ("Users preferring affordable food should receive affordable meal recommendations", "prefers(x,y)∧affordableMeal(y)", "obligation"),
    ("Users avoiding ultra processed food should not receive ultra processed food recommendations", "avoids(x,y)∧ultraProcessedFood(y)", "prohibition"),
    ("Users preferring local products may receive local food recommendations", "prefers(x,y)∧localProduct(y)", "permission"),
    ("Users preferring spicy food may receive spicy meal recommendations", "prefers(x,y)∧spicyMeal(y)", "permission"),
    ("Users avoiding spicy food should receive mild meal recommendations", "avoids(x,y)∧spicyMeal(y)∧mildMeal(y)", "obligation"),
    ("Users preferring mild food may receive mild meal recommendations", "prefers(x,y)∧mildMeal(y)", "permission"),
    ("Users avoiding sugary snacks should not receive sugary snack recommendations", "avoids(x,y)∧sugarySnack(y)", "prohibition"),
    ("Users avoiding salty snacks should not receive salty snack recommendations", "avoids(x,y)∧saltySnack(y)", "prohibition"),
    ("Users preferring Mediterranean cuisine should receive Mediterranean meal recommendations", "prefers(x,y)∧mediterraneanMeal(y)", "obligation"),
    ("Users preferring Asian cuisine may receive Asian meal recommendations", "prefers(x,y)∧asianMeal(y)", "permission"),
    ("Users preferring affordable Mediterranean meals should receive affordable Mediterranean recommendations", "prefers(x,y)∧mediterraneanMeal(y)∧affordableMeal(y)", "obligation"),
    ("Users preferring sustainable Asian meals may receive sustainable Asian recommendations", "prefers(x,y)∧asianMeal(y)∧sustainable(y)", "permission"),
    ("Users avoiding shellfish meals should not receive shellfish meal recommendations", "avoids(x,y)∧shellfishMeal(y)", "prohibition"),
    ("Adult users may receive energy drink recommendations", "adult(x)∧energyDrink(y)", "permission"),
    ("Adult users may receive spicy meal recommendations", "adult(x)∧spicyMeal(y)", "permission"),
    ("Adult users should receive nutrition labeled food recommendations when available", "adult(x)∧hasNutritionLabel(y)", "obligation"),
    ("Adult users avoiding high sugar products should not receive high sugar recommendations", "adult(x)∧avoids(x,y)∧highSugarProduct(y)", "prohibition"),
    ("Adult users preferring organic products may receive organic recommendations", "adult(x)∧prefers(x,y)∧organicFood(y)", "permission"),
    ("Users with low sugar requirements should receive low sugar food recommendations", "requiresLowSugar(x)∧lowSugarFood(y)", "obligation"),
    ("Users with low sugar requirements should not receive high sugar products", "requiresLowSugar(x)∧highSugarProduct(y)", "prohibition"),
    ("Users with low salt requirements should receive affordable low salt food recommendations", "requiresLowSalt(x)∧lowSaltFood(y)∧affordableMeal(y)", "obligation"),
    ("Users with low salt requirements should not receive high salt salty snacks", "requiresLowSalt(x)∧highSaltProduct(y)∧saltySnack(y)", "prohibition"),
    ("Users with health goals may receive healthy meal recommendations", "hasHealthGoal(x)∧healthyMeal(y)", "permission"),
    ("Users preferring protein rich meals should receive protein rich meal recommendations", "prefers(x,y)∧proteinRichMeal(y)", "obligation"),
    ("Users avoiding fried meals should not receive fried meal recommendations", "avoids(x,y)∧friedMeal(y)", "prohibition"),
    ("Users preferring low fat meals may receive low fat meal recommendations", "prefers(x,y)∧lowFatMeal(y)", "permission"),
    ("Users requiring heart healthy food should receive heart healthy meal recommendations", "requiresHeartHealthy(x)∧heartHealthyMeal(y)", "obligation"),
    ("Users avoiding caffeine should not receive caffeinated product recommendations", "avoids(x,y)∧caffeinatedProduct(y)", "prohibition"),
    ("Users preferring environmentally sustainable products should receive sustainable recommendations", "prefers(x,y)∧sustainable(y)∧environmentFriendly(y)", "obligation"),
    ("Users preferring budget meals may receive discounted meal recommendations", "prefers(x,y)∧discountedMeal(y)", "permission"),
    ("Users avoiding allergens should not receive products containing undeclared allergens", "avoids(x,y)∧containsUndeclaredAllergen(y)", "prohibition"),
    ("Users requiring certified products should receive certified product recommendations", "requiresCertifiedProduct(x)∧certified(y)", "obligation"),
    ("Users avoiding non certified products should not receive uncertified recommendations", "avoids(x,y)∧¬certified(y)", "prohibition"),
    ("Users preferring fresh food should receive fresh meal recommendations", "prefers(x,y)∧freshMeal(y)", "obligation"),
    ("Users avoiding processed meat should not receive processed meat recommendations", "avoids(x,y)∧processedMeat(y)", "prohibition"),
    ("Users preferring plant based meals may receive plant based recommendations", "prefers(x,y)∧plantBasedMeal(y)", "permission"),
    ("Users with combined low sugar and low salt needs should receive meals satisfying both needs", "requiresLowSugar(x)∧requiresLowSalt(x)∧lowSugarFood(y)∧lowSaltFood(y)", "obligation"),
    ("Users preferring seasonal food may receive seasonal meal recommendations", "prefers(x,y)∧seasonalMeal(y)", "permission"),
]


def formula(condition, norm_type, dyadic=False):
    modal = MODAL[norm_type]
    action = "recommend(System,y,x)"
    if dyadic:
        return f"∀x.∀y.{modal}({action}|{condition})"
    return f"∀x.∀y.{condition}->{modal}({action})"


def main():
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "stakeholder", "nl_norm", "implication_formula", "dyadic_formula", "norm_type"])
        for index, (nl_norm, condition, norm_type) in enumerate(ROWS, start=1):
            writer.writerow([
                f"USER{index:03d}",
                "User",
                nl_norm,
                formula(condition, norm_type, dyadic=False),
                formula(condition, norm_type, dyadic=True),
                norm_type,
            ])


if __name__ == "__main__":
    main()
