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
sponsored(y)
premiumProduct(y)
available(y)
recommend(System,y,x)
```

Incorrect:

```text
SponsoredProduct
PremiumMeal
recommend(System,SponsoredProduct)
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
NL: Eligible users should receive sponsored product recommendations when the product is available.
implication_formula: ∀x.∀y.eligible(x)∧sponsored(y)∧available(y)->O(recommend(System,y,x))
dyadic_formula: ∀x.∀y.O(recommend(System,y,x)|eligible(x)∧sponsored(y)∧available(y))
norm_type: obligation
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
- Product categories, product properties, and product eligibility must be predicates over `y`.
- User classes, market segments, and user requirements must be predicates over `x`.

# Dynamic Part: Food Industry Stakeholder

You are acting as the Food Industry stakeholder.

Use this stakeholder value for every record:

```text
Food Industry
```

Think like food producers, retailers, distributors, and brand owners. The norms should express commercial, product-placement, market-access, inventory, compliance, and brand-strategy expectations. Do not write them as personal user preferences or public-health regulations, except when industry compliance requires avoiding unsuitable recommendations.

Food Industry norms may reflect:

- sponsored product promotion
- premium product placement
- certified product visibility
- new product launches
- seasonal campaigns
- discounted products
- local product promotion
- sustainable product positioning
- inventory availability
- loyalty programs
- market segmentation
- brand-safe compliance
- product eligibility
- avoiding recommendations that would violate safety or labeling constraints

Include norms involving:

- sponsored products
- certified products
- premium products
- discounted products
- seasonal products
- new products
- local products
- sustainable products
- halal-certified products
- kosher-certified products
- gluten-free products
- lactose-free products
- organic products
- affordable products
- spicy and mild product segments
- Mediterranean and Asian product segments

Use these market and user predicates when relevant:

```text
eligible(x)
adult(x)
child(x)
loyalCustomer(x)
premiumCustomer(x)
interestedIn(x,LocalFood)
interestedIn(x,SustainableFood)
interestedIn(x,DiscountedFood)
interestedIn(x,SeasonalFood)
interestedIn(x,NewProduct)
interestedIn(x,Mediterranean)
interestedIn(x,Asian)
prefers(x,y)
avoids(x,y)
requiresHalal(x)
requiresKosher(x)
requiresGlutenFree(x)
requiresLactoseFree(x)
lactoseIntolerant(x)
glutenSensitive(x)
allergicTo(x,Nuts)
allergicTo(x,Shellfish)
```

Use these product and compliance predicates when relevant:

```text
sponsored(y)
certified(y)
premiumProduct(y)
discounted(y)
seasonal(y)
newProduct(y)
localProduct(y)
sustainable(y)
organic(y)
affordable(y)
available(y)
approved(y)
restricted(y)
safeFor(x,y)
contains(y,Nuts)
contains(y,Shellfish)
certifiedHalal(y)
certifiedKosher(y)
certifiedGlutenFree(y)
certifiedLactoseFree(y)
spicy(y)
mild(y)
mediterraneanMeal(y)
asianMeal(y)
```

Use IDs from `INDUSTRY001` to `INDUSTRY100`.

Output only CSV. Do not include explanations before or after the CSV.
