# Constitutive Rules Generation Prompt

Generate exactly 50 synthetic records for a constitutive rules dataset.

This is not a stakeholder norm dataset. It is a background domain-rule dataset. Constitutive rules define classifications or category relationships that can support reasoning over stakeholder norms.

Each record must contain:

id
scope
nl_rule
logic_rule
category

Use this exact CSV header:

```text
id,scope,nl_rule,logic_rule,category
```

## Purpose

The constitutive rules should define how specific food/product categories count as broader categories used in stakeholder norms.

For example, instead of writing many separate norms like:

```text
Vegan users should not receive shellfish meals.
Vegan users should not receive meat meals.
Vegan users should not receive dairy meals.
```

the system can use constitutive rules:

```text
∀y.shellfishMeal(y)->nonVegan(y)
∀y.meatMeal(y)->nonVegan(y)
∀y.dairyMeal(y)->nonVegan(y)
```

and one general stakeholder norm:

```text
∀x.∀y.vegan(x)∧nonVegan(y)->F(recommend(System,y,x))
```

## Formalization Style

Use `y` for products or food items.

Use implication formulas without modal operators:

```text
∀y.condition->classification(y)
```

Examples:

```text
∀y.shellfishMeal(y)->nonVegan(y)
∀y.meatMeal(y)->nonVegan(y)
∀y.energyDrink(y)->highSugarProduct(y)
∀y.nutSnack(y)->contains(y,Nuts)
∀y.shellfishMeal(y)∧contains(y,Shellfish)->nonVegan(y)
```

## Grammar Constraints

- Use only ASCII letters and digits inside predicate and term names.
- Do not use underscores.
- Do not use spaces inside formulas.
- Use `->` for implication, not `→`.
- Use `∧` for conjunction.
- Use `∨` for disjunction if needed.
- Use `¬` for negation only if necessary.
- Use quantifiers in every formula.
- Use `∀y.` for product classification rules.
- Every predicate with arguments must use parentheses.
- Do not use modal operators `O`, `P`, or `F` in constitutive rules.
- Do not use recommendation actions in constitutive rules.
- Do not use quoted strings in formulas.
- Do not use equality.
- Do not use arithmetic.

## Category Values

Use `category` values such as:

```text
dietaryClassification
allergenClassification
nutritionClassification
religiousClassification
medicalSuitability
productSafety
marketClassification
```

## Scope

Use this scope value for every record:

```text
FoodDomain
```

## Content Requirements

Include rules for:

- non-vegan classification
- non-vegetarian classification
- allergen-containing products
- high sugar products
- high salt products
- high fat products
- halal and non-halal classification
- kosher and non-kosher classification
- gluten-free and gluten-containing products
- lactose-free and dairy-containing products
- age-restricted products
- organic products
- sustainable products
- spicy and mild products
- cuisine categories

Use canonical predicates consistently. Do not create multiple names for the same concept.

Use IDs from `CR001` to `CR050`.

Output only CSV. Do not include explanations before or after the CSV.
