from lark import Lark

with open("grammar.lark", "r", encoding="utf-8") as f:
    grammar = f.read()

parser = Lark(
    grammar,
    start="formula",
    parser="lalr"
)

examples = [
    "∀x. F(recommend(System,EnergyDrink) | child(x))",
    "∀x. O(recommend(System,LowSugarFood) | diabetic(x))",
    "∀x. F(recommend(System,MeatMeal) | vegetarian(x))"
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