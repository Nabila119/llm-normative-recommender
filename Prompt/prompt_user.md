# Fixed Part: Dataset Task And Grammar

Generate exactly 100 synthetic records for a norm translation dataset.

This is not a recommendation dataset. It is a dataset for translating natural language stakeholder norms into deontic first-order logic.

Each record must contain:

id
stakeholder
formulation_type
nl_norm
logic_formula

The logic formula must use only this grammar-compatible syntax:

- Universal quantifier: ∀x. formula
- Existential quantifier: ∃x. formula
- Obligation: O(formula)
- Permission: P(formula)
- Prohibition: F(formula)
- Dyadic obligation: O(formula|formula)
- Dyadic permission: P(formula|formula)
- Dyadic prohibition: F(formula|formula)
- Implication: condition -> O(formula)
- Implication: condition -> P(formula)
- Implication: condition -> F(formula)
- Negation: ¬formula
- Conjunction: formula ∧ formula
- Disjunction: formula ∨ formula
- Predicates: predicate(term)
- Functions or compound terms: name(term1,term2)
- Atomic terms: names such as System, EnergyDrink, LowSugarFood, x

Important grammar constraints:

- Use only ASCII letters and digits inside names.
- Do not use underscores.
- Do not use spaces inside logic formulas.
- Use -> for implication, not →.
- Use ∧ for conjunction.
- Use ∨ for disjunction.
- Use ¬ for negation.
- Use | only inside modal formulas such as O(action|condition), P(action|condition), or F(action|condition).
- Every predicate with arguments must use parentheses.
- Constants and predicates must be written as single names, for example EnergyDrink, LowSugarFood, VeganMeal.
- Do not use quoted strings in formulas.
- Do not use equality.
- Do not use arithmetic.
- Do not use commas outside term lists.
- Do not concatenate multiple formulas without a connective.
- Use quantifiers in every formula.

Use formulation_type values only from:

dyadic_obligation
dyadic_permission
dyadic_prohibition
implication_obligation
implication_permission
implication_prohibition
simple_obligation
simple_permission
simple_prohibition

General dataset requirements:

- Include obligations, permissions, and prohibitions.
- Include both dyadic and implication-based norms.
- Include simple and complex norms.
- Include some formulas with one condition.
- Include some formulas with combined conditions using ∧.
- Include some formulas using ∨.
- Avoid duplicate natural language norms.
- Avoid duplicate logic formulas.
- Keep formulas concise and parser-compatible.

Canonical vocabulary rules:

- Use a consistent canonical naming scheme for all predicates, constants, and terms.
- Do not create multiple names for the same concept. For example, do not use both ShellfishAllergy and AllergyShellfish.
- Represent recommendation actions only as recommend(System,FoodItem).
- Do not encode properties inside predicate names when a predicate-term structure is available.
- Correct: allergicTo(x,Shellfish), contains(ShellfishMeal,Shellfish), highSugar(EnergyDrink).
- Incorrect: shellfishAllergy(x), ShellfishAllergy(x), allergyShellfish(x), isShellfishAllergic(x), highSugarEnergyDrink(x), EnergyDrinkHighSugar(x).
- If a new concept is needed, introduce exactly one clear canonical name and reuse it consistently throughout the dataset.
- Before finalizing the CSV, internally check that no two names refer to the same concept.

Output requirements:

- Generate exactly 100 records.
- Output only CSV.
- Use this exact header:
id,stakeholder,formulation_type,nl_norm,logic_formula
- Do not include explanations before or after the CSV.

# Dynamic Part: User Stakeholder

You are acting as the User stakeholder.

Use this stakeholder value for every record:

User

Think like individual users of a food recommender system. The norms should express user-side expectations, preferences, restrictions, permissions, obligations, and prohibitions.

User norms may reflect:

- personal health needs
- allergies
- ethical diets
- religious diets
- medical intolerances
- nutrition goals
- lifestyle preferences
- budget preferences
- taste preferences
- cuisine preferences
- avoidance preferences

Include at least some norms involving:

- halal food
- kosher food
- gluten-free food
- lactose-free food
- organic food
- sustainable food
- affordable food
- spicy food
- mild food
- Mediterranean food
- Asian food

Use formula patterns like:

∀x.F(recommend(System,EnergyDrink)|child(x))
∀x.diabetic(x)->O(recommend(System,LowSugarFood))
∀x.P(recommend(System,VeganMeal)|vegan(x))
∀x.child(x)∧allergicTo(x,Nuts)->F(recommend(System,NutSnack))
∀x.requiresHalal(x)->O(recommend(System,HalalMeal))

Use these canonical user-condition predicates when relevant:

allergicTo(x,Shellfish)
allergicTo(x,Nuts)
diabetic(x)
child(x)
adult(x)
elderly(x)
pregnant(x)
hypertensive(x)
vegetarian(x)
vegan(x)
requiresLowSugar(x)
requiresLowSalt(x)
requiresHalal(x)
requiresKosher(x)
requiresGlutenFree(x)
requiresLactoseFree(x)
lactoseIntolerant(x)
glutenSensitive(x)
prefers(x,FoodItem)
avoids(x,FoodItem)

Use these canonical food-property predicates when relevant:

highSugar(EnergyDrink)
highSalt(SaltySnack)
contains(NutSnack,Nuts)
contains(ShellfishMeal,Shellfish)
healthy(HealthyMeal)
approved(ApprovedFood)
restricted(RestrictedFood)
plantBased(VeganMeal)
nutritious(HealthyMeal)
halal(HalalMeal)
kosher(KosherMeal)
glutenFree(GlutenFreeMeal)
lactoseFree(LactoseFreeMeal)
organic(OrganicFood)
sustainable(SustainableMeal)
affordable(AffordableMeal)
localProduct(LocalProduct)
spicy(SpicyMeal)
mild(MildMeal)

Use these constants consistently when relevant:

EnergyDrink
LowSugarFood
LowSaltFood
HealthyMeal
VeganMeal
VegetarianMeal
NutSnack
ShellfishMeal
SaltySnack
SugarySnack
UltraProcessedFood
ApprovedFood
RestrictedFood
HalalMeal
NonHalalMeal
KosherMeal
NonKosherMeal
GlutenFreeMeal
WheatMeal
LactoseFreeMeal
DairyMeal
OrganicFood
SustainableMeal
AffordableMeal
LocalProduct
SpicyMeal
MildMeal
MediterraneanMeal
AsianMeal

Use IDs from USER001 to USER100.
