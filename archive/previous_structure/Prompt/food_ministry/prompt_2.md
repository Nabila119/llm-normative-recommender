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
- Constants and predicates must be written as single names, for example EnergyDrink, LowSugarFood, HealthyMeal.
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
- Correct: allergicTo(x,Shellfish), contains(ShellfishMeal,Shellfish), exceedsSugarLimit(EnergyDrink).
- Incorrect: shellfishAllergy(x), ShellfishAllergy(x), allergyShellfish(x), highSugarEnergyDrink(x), EnergyDrinkHighSugar(x).
- If a new concept is needed, introduce exactly one clear canonical name and reuse it consistently throughout the dataset.
- Before finalizing the CSV, internally check that no two names refer to the same concept.

Output requirements:

- Generate exactly 100 records.
- Output only CSV.
- Use this exact header:
id,stakeholder,formulation_type,nl_norm,logic_formula
- Do not include explanations before or after the CSV.

# Dynamic Part: Food Ministry Stakeholder

You are acting as the Food Ministry stakeholder.

Use this stakeholder value for every record:

Food Ministry

Think like a public regulator responsible for food safety, public health, nutrition standards, labeling rules, consumer protection, and protection of vulnerable populations. Do not write the norms as personal user preferences. Write them as regulatory requirements, permissions, prohibitions, and safeguards that a food recommender system must follow.

Food Ministry norms may reflect:

- public health protection
- vulnerable population safeguards
- nutrition thresholds
- age-based restrictions
- allergen disclosure
- food safety warnings
- labeling compliance
- misleading-claim prevention
- approved and restricted product classes
- disease-risk reduction
- fair access to healthy food
- accommodation of religious, medical, and cultural dietary requirements

Include at least some norms involving:

- children and age-restricted foods
- diabetic users and sugar limits
- hypertensive users and salt limits
- pregnant users and safety warnings
- elderly users and healthy alternatives
- users with allergies and declared allergens
- halal and kosher labeling compliance
- gluten-free and lactose-free labeling compliance
- misleading organic or sustainability claims
- affordable healthy food access

Use formula patterns like:

∀x.F(recommend(System,EnergyDrink)|child(x)∧exceedsSugarLimit(EnergyDrink))
∀x.diabetic(x)->O(recommend(System,LowSugarFood))
∀x.allergicTo(x,Nuts)∧containsUndeclaredAllergen(NutSnack)->F(recommend(System,NutSnack))
∀x.P(recommend(System,ApprovedFood)|adult(x)∧compliesWithGuideline(ApprovedFood))
∀x.requiresHalal(x)∧¬verifiedHalal(HalalMeal)->F(recommend(System,HalalMeal))

Use these canonical population predicates when relevant:

child(x)
adult(x)
elderly(x)
pregnant(x)
diabetic(x)
hypertensive(x)
allergicTo(x,Nuts)
allergicTo(x,Shellfish)
requiresHalal(x)
requiresKosher(x)
requiresGlutenFree(x)
requiresLactoseFree(x)
lactoseIntolerant(x)
glutenSensitive(x)
vulnerableUser(x)

Use these canonical regulatory predicates when relevant:

approvedByMinistry(ApprovedFood)
restricted(RestrictedFood)
bannedForChildren(EnergyDrink)
exceedsSugarLimit(EnergyDrink)
exceedsSugarLimit(SugarySnack)
exceedsSaltLimit(SaltySnack)
exceedsFatLimit(FriedMeal)
contains(NutSnack,Nuts)
contains(ShellfishMeal,Shellfish)
containsUndeclaredAllergen(NutSnack)
containsUndeclaredAllergen(ShellfishMeal)
hasNutritionLabel(ApprovedFood)
hasSafetyWarning(EnergyDrink)
requiresWarning(EnergyDrink)
compliesWithGuideline(ApprovedFood)
misleadingClaim(OrganicFood)
verifiedHalal(HalalMeal)
verifiedKosher(KosherMeal)
certifiedGlutenFree(GlutenFreeMeal)
certifiedLactoseFree(LactoseFreeMeal)
safeForPregnantUsers(HealthyMeal)
safeForDiabeticUsers(LowSugarFood)
healthy(HealthyMeal)
affordable(AffordableMeal)

Use these constants consistently when relevant:

EnergyDrink
SugarySnack
SaltySnack
FriedMeal
LowSugarFood
LowSaltFood
HealthyMeal
ApprovedFood
RestrictedFood
NutSnack
ShellfishMeal
HalalMeal
KosherMeal
GlutenFreeMeal
LactoseFreeMeal
OrganicFood
SustainableMeal
AffordableMeal
WarningFood

Use IDs from MINISTRY001 to MINISTRY100.
