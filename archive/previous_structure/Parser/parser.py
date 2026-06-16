from lark import Lark

with open("grammar.lark", "r", encoding="utf-8") as f:
    grammar = f.read()

parser = Lark(
    grammar,
    start="formula",
    parser="lalr"
)

examples = [
    # Revised implication-based normative formulas
    "∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))",
    "∀x.∀y.diabetic(x)∧lowSugarFood(y)->O(recommend(System,y,x))",
    "∀x.∀y.requiresGlutenFree(x)∧glutenFreeMeal(y)∧certifiedGlutenFree(y)->P(recommend(System,y,x))",

    # Revised dyadic normative formulas
    "∀x.∀y.F(recommend(System,y,x)|child(x)∧energyDrink(y))",
    "∀x.∀y.O(recommend(System,y,x)|diabetic(x)∧lowSugarFood(y))",
    "∀x.∀y.P(recommend(System,y,x)|requiresGlutenFree(x)∧glutenFreeMeal(y)∧certifiedGlutenFree(y))",

    # Constitutive rules
    "∀y.shellfishMeal(y)->nonVegan(y)",
    "∀y.shellfishMeal(y)∧contains(y,Shellfish)->nonVegan(y)",
    "∀y.energyDrink(y)->highSugarProduct(y)",
    "∀y.nutSnack(y)->contains(y,Nuts)"
]

for formula in examples:

    print("\n========================")
    print("Formula:")
    print(formula)

    try:
        tree = parser.parse(formula)

        print("\nVALID")
        print(tree.pretty())

    except Exception as e:

        print("\nINVALID")
        print(e)
