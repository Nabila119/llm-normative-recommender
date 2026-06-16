# Revised Formula Patterns

This file defines representative formula patterns for the revised dataset design after supervisor feedback. These patterns should be used before generating the full datasets to ensure that the grammar, parser, prompts, and AST generator all target the same formal language.

## Modeling Conventions

- `x` ranges over users.
- `y` ranges over products or food items.
- Product categories are predicates over product variables, for example `energyDrink(y)` and `glutenFreeMeal(y)`.
- The recommendation relation includes the target user: `recommend(System,y,x)`.
- Main stakeholder norm records should contain both an implication-based formula and a dyadic formula for the same natural language norm.
- Constitutive rules are stored separately from stakeholder norm records.

## Normative Implication Patterns

Prohibition:

```text
∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))
```

Obligation:

```text
∀x.∀y.diabetic(x)∧lowSugarFood(y)->O(recommend(System,y,x))
```

Permission:

```text
∀x.∀y.requiresGlutenFree(x)∧glutenFreeMeal(y)∧certifiedGlutenFree(y)->P(recommend(System,y,x))
```

## Normative Dyadic Patterns

Dyadic prohibition:

```text
∀x.∀y.F(recommend(System,y,x)|child(x)∧energyDrink(y))
```

Dyadic obligation:

```text
∀x.∀y.O(recommend(System,y,x)|diabetic(x)∧lowSugarFood(y))
```

Dyadic permission:

```text
∀x.∀y.P(recommend(System,y,x)|requiresGlutenFree(x)∧glutenFreeMeal(y)∧certifiedGlutenFree(y))
```

## Constitutive Rule Patterns

Simple category rule:

```text
∀y.shellfishMeal(y)->nonVegan(y)
```

Conjunctive category rule:

```text
∀y.shellfishMeal(y)∧contains(y,Shellfish)->nonVegan(y)
```

Product property rule:

```text
∀y.energyDrink(y)->highSugarProduct(y)
```

Ingredient classification rule:

```text
∀y.nutSnack(y)->contains(y,Nuts)
```

## Pilot Dataset Check

Before generating the full datasets, the parser should validate:

- all implication formulas
- all dyadic formulas
- all constitutive rules
- formulas with multiple quantifiers
- formulas with compound conditions
- formulas using `recommend(System,y,x)`

