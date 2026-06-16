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

Do not represent product categories as constants. Product categories and product properties must be predicates over `y`.

Correct:

```text
energyDrink(y)
exceedsSugarLimit(y)
approvedByMinistry(y)
recommend(System,y,x)
```

Incorrect:

```text
EnergyDrink
ApprovedFood
recommend(System,EnergyDrink)
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
NL: Children must not receive products exceeding sugar limits.
implication_formula: ∀x.∀y.child(x)∧exceedsSugarLimit(y)->F(recommend(System,y,x))
dyadic_formula: ∀x.∀y.F(recommend(System,y,x)|child(x)∧exceedsSugarLimit(y))
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
- Product categories and regulatory properties must be predicates over `y`.
- User classes and requirements must be predicates over `x`.

# Dynamic Part: Food Ministry Stakeholder

You are acting as the Food Ministry stakeholder.

Use this stakeholder value for every record:

```text
Food Ministry
```

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

Include norms involving:

- children and age-restricted products
- diabetic users and sugar limits
- hypertensive users and salt limits
- pregnant users and safety warnings
- elderly users and healthy alternatives
- allergic users and declared allergens
- halal and kosher labeling compliance
- gluten-free and lactose-free certification
- misleading organic or sustainability claims
- affordable healthy food access

Use these population predicates when relevant:

```text
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
```

Use these regulatory and product predicates when relevant:

```text
approvedByMinistry(y)
restricted(y)
bannedForChildren(y)
exceedsSugarLimit(y)
exceedsSaltLimit(y)
exceedsFatLimit(y)
contains(y,Nuts)
contains(y,Shellfish)
containsUndeclaredAllergen(y)
hasNutritionLabel(y)
hasSafetyWarning(y)
requiresWarning(y)
compliesWithGuideline(y)
misleadingClaim(y)
verifiedHalal(y)
verifiedKosher(y)
certifiedGlutenFree(y)
certifiedLactoseFree(y)
safeForPregnantUsers(y)
safeForDiabeticUsers(y)
healthyMeal(y)
affordableMeal(y)
energyDrink(y)
sugarySnack(y)
saltySnack(y)
friedMeal(y)
```

Use IDs from `MINISTRY001` to `MINISTRY100`.

Output only CSV. Do not include explanations before or after the CSV.
