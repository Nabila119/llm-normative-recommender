# Claude vs Baseline Dataset Comparison

Claude metadata supplied by Viktor:

- LLM: Claude
- Model/version: Claude Opus 4.8, High effort
- Stakeholder datasets generated: 2026-06-28
- Constitutive rules generated: 2026-07-03
- Prompt files used: GitHub stakeholder prompt files and `prompts/prompt_constitutive_rules.md`
- Fresh chat: yes
- Manual edits: none

## Validation Result

The Claude stakeholder datasets and Claude constitutive rules were validated using the same `scripts/validate_revised_datasets.py` parser validation used for the baseline revised datasets.

| Source | Records | Formulas | Errors | Warnings |
|---|---:|---:|---:|---:|
| Baseline revised full dataset | 350 | 650 | 0 | 0 |
| Claude full dataset | 350 | 650 | 0 | 0 |

## Round-Trip Automatic Evaluation

| Source | Rows | Score 2 | Score 1 | Score 0 |
|---|---:|---:|---:|---:|
| Baseline revised stakeholder datasets | 600 | 538 | 40 | 22 |
| Claude stakeholder datasets | 600 | 550 | 46 | 4 |

These automatic scores are heuristic triage results. Human review is still required for semantic accuracy.

## Summary by Stakeholder

| Stakeholder | Claude rows | Claude formulas | Exact NL overlap | Exact implication overlap | Exact dyadic overlap | Shared predicates | Avg condition size baseline | Avg condition size Claude |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| User | 100 | 200 | 0 | 22 | 22 | 46 | 2.23 | 2.12 |
| Food Ministry | 100 | 200 | 0 | 14 | 14 | 37 | 2.14 | 2.5 |
| Food Industry | 100 | 200 | 0 | 6 | 6 | 39 | 2.33 | 2.04 |

## Norm-Type Distribution

### User

- Baseline: obligation: 36, permission: 27, prohibition: 37
- Claude: obligation: 15, permission: 43, prohibition: 42

### Food Ministry

- Baseline: obligation: 31, permission: 24, prohibition: 45
- Claude: obligation: 25, permission: 35, prohibition: 40

### Food Industry

- Baseline: obligation: 38, permission: 36, prohibition: 26
- Claude: obligation: 34, permission: 38, prohibition: 28

## Constitutive Rules Comparison

| Dataset | Claude rows | Exact NL overlap | Exact logic overlap | Exact category overlap | Shared predicates |
|---|---:|---:|---:|---:|---:|
| Constitutive Rules | 50 | 0 | 8 | 7 | 24 |

- Baseline categories: allergenClassification: 5, dietaryClassification: 10, marketClassification: 5, medicalSuitability: 6, nutritionClassification: 15, productSafety: 3, religiousClassification: 6
- Claude categories: allergenClassification: 7, dietaryClassification: 16, marketClassification: 7, medicalSuitability: 1, nutritionClassification: 8, productSafety: 3, religiousClassification: 8
- Baseline predicate count: 56
- Claude predicate count: 53
- Baseline-only predicate examples: alcoholProduct, almondDessert, beefMeal, breadProduct, butterProduct, candyProduct, cannedSoup, cheeseMeal, chickenMeal, creamDessert, cuisineSpecificProduct, eggMeal, fastFoodMeal, honeyProduct, instantNoodles, marketPreferenceProduct, milkProduct, nonCertifiedMeat, peanutSnack, porkMeal, processedMeat, regularPasta, regularSoda, safetyWarningProduct, saltedNuts, seasonalMeal, shrimpMeal, sweetDessert, uncertainHalalStatus, uncertainKosherStatus
- Claude-only predicate examples: allergenContaining, bannedForChildren, certifiedGlutenFree, certifiedHalal, certifiedKosher, certifiedLactoseFree, exceedsFatLimit, exceedsSaltLimit, exceedsSugarLimit, glutenContaining, glutenFreeMeal, halalMeal, healthyMeal, internationalCuisineMeal, kosherMeal, lactoseFreeMeal, localProduct, mild, mildMeal, organic, safeFor, spicy, spicyMeal, sustainableMeal, ultraProcessedFood, veganMeal, vegetarianMeal, verifiedHalal, verifiedKosher

## Predicate Vocabulary Differences

### User

- Baseline predicate count: 83
- Claude predicate count: 48
- Shared predicates: 46
- Baseline-only examples: allergenSafeMeal, caffeinatedProduct, certified, certifiedHealthy, containsUndeclaredAllergen, dairyMeal, discountedMeal, environmentFriendly, freshMeal, friedMeal, hasHealthGoal, hasNutritionLabel, heartHealthyMeal, highSaltProduct, highSugarProduct, localProduct, lowFatMeal, meatMeal, nonHalal, nonKosher, nonVegetarian, nutFreeMeal, plantBasedMeal, processedMeat, proteinRichMeal, requiresCertifiedProduct, requiresHeartHealthy, requiresWarning, safeForPregnantUsers, seasonalMeal
- Claude-only examples: nutSnack, sustainableMeal

### Food Ministry

- Baseline predicate count: 77
- Claude predicate count: 40
- Shared predicates: 37
- Baseline-only examples: ageRestrictedProduct, allergenSafeMeal, alternativeToRestrictedFood, available, avoids, certified, completeLabel, compliesWithLabeling, essentialFood, halalMeal, hasAllergenLabel, highFatProduct, highSaltProduct, highSugarProduct, incompleteLabel, kosherMeal, lowFatMeal, lowSaltFood, lowSugarFood, meetsNutritionGuideline, nonHalal, nonKosher, nutritionClaim, organicFood, prefers, requiresCertifiedProduct, requiresLowSalt, requiresLowSugar, safeFor, safetyWarningProduct
- Claude-only examples: friedMeal, saltySnack, sugarySnack

### Food Industry

- Baseline predicate count: 48
- Claude predicate count: 39
- Shared predicates: 39
- Baseline-only examples: brandSafe, brandUnsafe, cuisineSpecificProduct, healthyMeal, marketPreferenceProduct, misleadingClaim, requiresCertifiedProduct, unaffordable, verifiedClaim
- Claude-only examples: -

## Initial Interpretation

Both datasets pass syntactic validation under the fixed grammar. This means Claude was able to follow the grammar and revised formula conventions for the stakeholder datasets and the constitutive background rules.

The more important comparison is now semantic and design-oriented: whether Claude's norms are as stakeholder-specific, diverse, and useful for conflict detection as the baseline dataset. Exact formula overlap is expected to be limited because Claude generated new records from the same prompt rather than reproducing the baseline rows exactly.

Recommended next step: perform human semantic review on a sample of baseline and Claude round-trip rows, especially rows with automatic scores 0 or 1, and then compare whether the smaller Claude predicate vocabulary affects conflict-detection usefulness.