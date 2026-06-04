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
- Atomic terms: names such as System, SponsoredProduct, PremiumMeal, x

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
- Constants and predicates must be written as single names, for example SponsoredProduct, SeasonalFood, CertifiedMeal.
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
- Do not create multiple names for the same concept. For example, do not use both SponsoredProduct and ProductSponsored for the same meaning.
- Represent recommendation actions only as recommend(System,FoodItem).
- Do not encode properties inside predicate names when a predicate-term structure is available.
- Correct: sponsored(SponsoredProduct), available(LocalProduct), certified(CertifiedMeal).
- Incorrect: sponsoredProduct(x), ProductSponsored(SponsoredProduct), certifiedMeal(x), availableLocalProduct(x).
- If a new concept is needed, introduce exactly one clear canonical name and reuse it consistently throughout the dataset.
- Before finalizing the CSV, internally check that no two names refer to the same concept.

Output requirements:

- Generate exactly 100 records.
- Output only CSV.
- Use this exact header:
id,stakeholder,formulation_type,nl_norm,logic_formula
- Do not include explanations before or after the CSV.

# Dynamic Part: Food Industry Stakeholder

You are acting as the Food Industry stakeholder.

Use this stakeholder value for every record:

Food Industry

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

Include at least some norms involving:

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

Use formula patterns like:

∀x.O(recommend(System,SponsoredProduct)|eligible(x)∧sponsored(SponsoredProduct))
∀x.loyalCustomer(x)->P(recommend(System,PremiumMeal))
∀x.allergicTo(x,Nuts)->F(recommend(System,NutSnack))
∀x.interestedIn(x,LocalFood)∧available(LocalProduct)->O(recommend(System,LocalProduct))
∀x.requiresHalal(x)∧certifiedHalal(HalalMeal)->P(recommend(System,HalalMeal))

Use these canonical market/user predicates when relevant:

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
prefers(x,FoodItem)
avoids(x,FoodItem)
requiresHalal(x)
requiresKosher(x)
requiresGlutenFree(x)
requiresLactoseFree(x)
lactoseIntolerant(x)
glutenSensitive(x)
allergicTo(x,Nuts)
allergicTo(x,Shellfish)

Use these canonical product and compliance predicates when relevant:

sponsored(SponsoredProduct)
certified(CertifiedMeal)
premiumProduct(PremiumMeal)
discounted(DiscountedFood)
seasonal(SeasonalFood)
newProduct(NewProduct)
localProduct(LocalProduct)
sustainable(SustainableMeal)
organic(OrganicFood)
affordable(AffordableMeal)
available(SponsoredProduct)
available(LocalProduct)
available(SeasonalFood)
approved(ApprovedFood)
restricted(RestrictedFood)
safeFor(x,FoodItem)
contains(NutSnack,Nuts)
contains(ShellfishMeal,Shellfish)
certifiedHalal(HalalMeal)
certifiedKosher(KosherMeal)
certifiedGlutenFree(GlutenFreeMeal)
certifiedLactoseFree(LactoseFreeMeal)
spicy(SpicyMeal)
mild(MildMeal)
cuisine(MediterraneanMeal,Mediterranean)
cuisine(AsianMeal,Asian)

Use these constants consistently when relevant:

SponsoredProduct
CertifiedMeal
PremiumMeal
DiscountedFood
SeasonalFood
NewProduct
LocalProduct
SustainableMeal
OrganicFood
AffordableMeal
ApprovedFood
RestrictedFood
NutSnack
ShellfishMeal
HalalMeal
KosherMeal
GlutenFreeMeal
LactoseFreeMeal
SpicyMeal
MildMeal
MediterraneanMeal
AsianMeal
LocalFood
SustainableFood
DiscountedFood
Mediterranean
Asian

Use IDs from INDUSTRY001 to INDUSTRY100.
