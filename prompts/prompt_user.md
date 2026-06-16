# Fixed Part: Dataset Task And Grammar

Generate exactly 100 synthetic records for a stakeholder norm translation dataset.

This is not a recommendation dataset. It is a dataset for translating natural language stakeholder norms into modal/deontic first-order logic.

Each record must contain:

id
stakeholder
nl_norm
implication_formula
dyadic_formula
norm_type

Use this exact CSV header:

```text
id,stakeholder,nl_norm,implication_formula,dyadic_formula,norm_type
```

The `implication_formula` and `dyadic_formula` must formalize the same natural language norm.

## Required Formalization Style

Use `x` for users.
Use `y` for products or food items.
Represent recommendation as:

```text
recommend(System,y,x)
```

This means that the system recommends product `y` to user `x`.

Do not represent product categories as constants.

Correct:

```text
energyDrink(y)
glutenFreeMeal(y)
lowSugarFood(y)
certifiedGlutenFree(y)
recommend(System,y,x)
```

Incorrect:

```text
EnergyDrink
GlutenFreeMeal
LowSugarFood
recommend(System,EnergyDrink)
recommend(System,GlutenFreeMeal)
```

## Formula Requirements

For every natural language norm, generate both:

1. An implication-based monadic formula.
2. A dyadic formula.

Implication pattern:

```text
∀x.∀y.condition->O(recommend(System,y,x))
∀x.∀y.condition->P(recommend(System,y,x))
∀x.∀y.condition->F(recommend(System,y,x))
```

Dyadic pattern:

```text
∀x.∀y.O(recommend(System,y,x)|condition)
∀x.∀y.P(recommend(System,y,x)|condition)
∀x.∀y.F(recommend(System,y,x)|condition)
```

Example:

```text
NL: Children should not receive energy drink recommendations.
implication_formula: ∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))
dyadic_formula: ∀x.∀y.F(recommend(System,y,x)|child(x)∧energyDrink(y))
norm_type: prohibition
```

## Grammar Constraints

- Use only ASCII letters and digits inside predicate and term names.
- Do not use underscores.
- Do not use spaces inside formulas.
- Use `->` for implication, not `→`.
- Use `∧` for conjunction.
- Use `∨` for disjunction.
- Use `¬` for negation.
- Use `|` only inside dyadic modal formulas.
- Use quantifiers in every formula.
- Use `∀x.∀y.` for stakeholder norms involving users and products.
- Every predicate with arguments must use parentheses.
- Do not use quoted strings in formulas.
- Do not use equality.
- Do not use arithmetic.
- Do not concatenate multiple formulas without a connective.

Use `norm_type` values only from:

```text
obligation
permission
prohibition
```

## Dataset Requirements

- Include obligations, permissions, and prohibitions.
- Include simple and complex conditions.
- Include some formulas with one condition.
- Include some formulas with combined conditions using `∧`.
- Include some formulas using `∨`.
- Avoid duplicate natural language norms.
- Avoid duplicate formulas.
- Keep formulas concise and parser-compatible.
- Do not include constitutive rules in this dataset. Constitutive rules belong in a separate file.

## Canonical Vocabulary Rules

- Use one canonical predicate for each concept.
- Do not create multiple names for the same concept.
- Do not encode properties inside constants.
- Product categories and product properties must be predicates over `y`.
- User properties and user requirements must be predicates over `x`.

Correct:

```text
allergicTo(x,Nuts)
contains(y,Nuts)
vegan(x)
nonVegan(y)
requiresHalal(x)
halalMeal(y)
certifiedHalal(y)
```

Incorrect:

```text
NutAllergy(x)
AllergyNuts(x)
NutSnack
HalalMeal
CertifiedHalalMeal
```

# Dynamic Part: User Stakeholder

You are acting as the User stakeholder.

Use this stakeholder value for every record:

```text
User
```

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

Include norms involving:

- children
- adults
- elderly users
- pregnant users
- diabetic users
- hypertensive users
- users allergic to nuts
- users allergic to shellfish
- vegan users
- vegetarian users
- halal requirements
- kosher requirements
- gluten-free requirements
- lactose-free requirements
- low sugar needs
- low salt needs
- affordable food preferences
- spicy and mild food preferences
- Mediterranean and Asian cuisine preferences

Use these user predicates when relevant:

```text
child(x)
adult(x)
elderly(x)
pregnant(x)
diabetic(x)
hypertensive(x)
vegan(x)
vegetarian(x)
allergicTo(x,Nuts)
allergicTo(x,Shellfish)
requiresLowSugar(x)
requiresLowSalt(x)
requiresHalal(x)
requiresKosher(x)
requiresGlutenFree(x)
requiresLactoseFree(x)
lactoseIntolerant(x)
glutenSensitive(x)
prefers(x,y)
avoids(x,y)
```

Use these product predicates when relevant:

```text
energyDrink(y)
lowSugarFood(y)
lowSaltFood(y)
healthyMeal(y)
veganMeal(y)
vegetarianMeal(y)
nutSnack(y)
shellfishMeal(y)
saltySnack(y)
sugarySnack(y)
ultraProcessedFood(y)
halalMeal(y)
kosherMeal(y)
glutenFreeMeal(y)
lactoseFreeMeal(y)
organicFood(y)
sustainableMeal(y)
affordableMeal(y)
spicyMeal(y)
mildMeal(y)
mediterraneanMeal(y)
asianMeal(y)
certifiedHalal(y)
certifiedKosher(y)
certifiedGlutenFree(y)
certifiedLactoseFree(y)
contains(y,Nuts)
contains(y,Shellfish)
```

Use IDs from `USER001` to `USER100`.

Output only CSV. Do not include explanations before or after the CSV.
