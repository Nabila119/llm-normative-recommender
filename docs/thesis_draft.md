# Leveraging LLMs for Agent-Based Normative Recommender Systems

## Working Thesis Draft

This document is a living thesis draft. It is intended to be developed alongside the implementation work so that dataset design, parser development, validation results, and experimental decisions are documented as they are made.

## 1. Introduction

Recommender systems increasingly influence choices in domains where recommendations are not only a matter of preference, but also of safety, health, compliance, and social acceptability. Food recommendation is a clear example of this problem. A food recommender may need to consider allergies, medical conditions, religious dietary requirements, public-health rules, product-labeling constraints, and commercial interests at the same time. These requirements often come from different stakeholders and may conflict with one another.

This thesis investigates how large language models can support the formalization of stakeholder norms for agent-based normative food recommender systems. The focus is not on predicting which food item a user will like. Instead, the central problem is how natural language norms can be translated into a controlled modal first-order logic representation that can be parsed, inspected, transformed into an abstract syntax tree, and used for conflict analysis.

The work is motivated by the gap between informal stakeholder requirements and formal reasoning tools. Stakeholders may express norms in natural language, such as "children should not receive energy drink recommendations" or "users requiring gluten-free food may receive certified gluten-free meals." Such statements are understandable to humans but difficult to validate or compare computationally. Formalization makes the normative structure explicit by identifying the user, the product, the recommendation action, the condition, and the deontic status of the action.

The thesis therefore studies a pipeline for norm formalization and analysis. Natural language stakeholder norms are translated into modal first-order logic formulas, validated against a fixed grammar, transformed into AST representations, evaluated through round-trip semantic preservation, and prepared for conflict detection. A particular focus is placed on the difference between implication-based monadic formulations, such as `X->O(Y)`, and dyadic formulations, such as `O(Y|X)`. These forms are not assumed to be semantically identical; rather, they are treated as alternative formalization strategies whose practical behavior can be compared.

## 2. Research Context

The system context considered in this thesis is an agent-based food recommender system. The recommender is treated as an agent whose recommendations may be subject to norms from multiple stakeholders. Three stakeholder perspectives are considered:

- User
- Food Ministry
- Food Industry

Each stakeholder may impose different kinds of norms. Users may express personal preferences, dietary restrictions, religious requirements, medical constraints, allergies, budget preferences, and taste preferences. A Food Ministry may impose public-health and regulatory norms concerning vulnerable groups, nutrition thresholds, allergen disclosure, product restrictions, and labeling compliance. Food Industry actors may express commercial and product-placement norms concerning sponsored products, certified products, seasonal products, premium products, and market segmentation, while still respecting compliance constraints.

The goal is to study whether LLMs can translate such stakeholder norms into a controlled logical language suitable for computational validation and reasoning, while also preserving stakeholder meaning and producing structures that are useful for conflict detection.

## 3. Dataset Construction

### 3.1 Dataset Purpose

The dataset constructed for this thesis is a norm translation dataset. It is not a recommendation dataset. Each record pairs a natural language stakeholder norm with formal logic representations of that norm. The dataset is designed to support evaluation of LLM-based norm formalization.

The revised main stakeholder dataset uses the following schema:

```text
id
stakeholder
nl_norm
implication_formula
dyadic_formula
norm_type
```

The `stakeholder` field identifies the source perspective of the norm. The `nl_norm` field contains the natural language norm. The `implication_formula` field contains an implication-based monadic formalization, while the `dyadic_formula` field contains a dyadic formalization of the same norm. The `norm_type` field identifies whether the norm is an obligation, permission, or prohibition.

This paired design allows the same natural language norm to be represented in both formalization styles. This is important because implication-based and dyadic formulations are not treated as interchangeable notations. Instead, they are compared in terms of syntactic validity, AST structure, semantic preservation, and suitability for conflict detection.

### 3.2 Stakeholder-Specific Datasets

Three stakeholder datasets were constructed:

- User dataset: 100 records
- Food Ministry dataset: 100 records
- Food Industry dataset: 100 records

The User dataset captures norms from the perspective of individual users. These include health needs, allergies, ethical diets, religious diets, medical intolerances, nutrition goals, lifestyle preferences, budget preferences, taste preferences, cuisine preferences, and avoidance preferences.

The Food Ministry dataset captures norms from the perspective of a public regulator. These norms focus on food safety, public health, nutrition thresholds, labeling compliance, allergen disclosure, misleading claims, protection of vulnerable populations, and access to healthy food.

The Food Industry dataset captures norms from the perspective of producers, retailers, distributors, and brand owners. These norms focus on product promotion, sponsored products, premium placement, certified products, market segmentation, availability, seasonal campaigns, local products, sustainable products, and compliance-related restrictions.

### 3.3 Paired Formalization Types

The dataset includes two formal representations for each conditional norm:

- implication-based monadic formulation: `X->O(Y)`, `X->P(Y)`, or `X->F(Y)`
- dyadic formulation: `O(Y|X)`, `P(Y|X)`, or `F(Y|X)`

This distinction is important because a norm can often be expressed in more than one logically plausible way, but the two representations have different semantic interpretations. For example, a conditional prohibition can be represented as an implication-based norm:

```text
∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))
```

or as a dyadic norm:

```text
∀x.∀y.F(recommend(System,y,x)|child(x)∧energyDrink(y))
```

Both formulas may correspond to the same natural language sentence, but they differ structurally and semantically. This affects parsing, AST generation, round-trip translation, and conflict detection. For this reason, the thesis does not collapse the two representations into a single notation. Instead, both are preserved so their practical consequences can be studied.

### 3.4 Product Variables And Predicate-Based Categories

A revised modeling decision is to avoid treating product categories as constants. A term such as `GlutenFreeMeal` should not be used as if it denoted the entire class of gluten-free meals, because in first-order logic a constant normally refers to a specific object in the model. Instead, product categories are represented as predicates over product variables.

For example, the following earlier style of formula is too specific and is no longer the preferred representation:

```text
∀x.requiresGlutenFree(x)->P(recommend(System,GlutenFreeMeal))
```

Here `GlutenFreeMeal` is treated as a constant, which would refer to one particular object rather than to all gluten-free meals. A more appropriate representation quantifies over products:

```text
∀x.∀y.requiresGlutenFree(x)∧glutenFreeMeal(y)∧certifiedGlutenFree(y)->P(recommend(System,y,x))
```

In this formula, `x` ranges over users and `y` ranges over products. The predicate `glutenFreeMeal(y)` states that product `y` is a gluten-free meal, and `certifiedGlutenFree(y)` states that it is certified as gluten-free. The recommendation relation is represented as `recommend(System,y,x)`, meaning that the system recommends product `y` to user `x`.

The truth of predicates such as `glutenFreeMeal(y)` or `certifiedGlutenFree(y)` is not stored directly in the norm translation dataset. Such truth values would be supplied by a domain interpretation, such as a product catalog, food ontology, or knowledge base. The focus of this thesis is the translation and structural analysis of norms, not the construction of a full product database. However, small illustrative product and user facts may be used later to demonstrate grounding and conflict examples.

### 3.5 Canonical Vocabulary

A controlled canonical vocabulary was used during dataset construction. This was necessary to avoid ambiguous or duplicate representations of the same concept. For example, the same allergy should not appear under multiple names such as:

```text
ShellfishAllergy
AllergyShellfish
isShellfishAllergic
```

Instead, the canonical representation is:

```text
allergicTo(x,Shellfish)
```

The dataset therefore favors predicate-term structures over encoded predicate names. For example:

```text
contains(y,Shellfish)
energyDrink(y)
requiresHalal(x)
certifiedGlutenFree(y)
```

This design improves consistency across records and reduces unnecessary lexical variation. It also supports more reliable parsing and later comparison between formulas.

### 3.6 Constitutive Rules

Some domain knowledge is better represented through constitutive rules rather than repeated stakeholder norms. Constitutive rules define classifications or meanings, while normative rules express obligations, permissions, or prohibitions.

For example, instead of writing separate prohibitions for vegan users and every non-vegan product category, a constitutive rule can define that shellfish meals count as non-vegan:

```text
∀y.shellfishMeal(y)->nonVegan(y)
```

The normative rule can then be stated more generally:

```text
∀x.∀y.vegan(x)∧nonVegan(y)->F(recommend(System,y,x))
```

This reduces redundancy and supports more systematic conflict detection. In the revised design, constitutive rules are kept in a separate supporting dataset rather than mixed into the main stakeholder norm dataset. The main dataset contains stakeholder norms involving obligations, permissions, and prohibitions, while the constitutive dataset contains background classification rules.

### 3.7 Reproducibility Of Dataset Generation

The dataset generation process was designed to be reproducible, but there is an important distinction between procedural reproducibility and exact experimental reproducibility.

The prompts document the procedure used to generate the datasets. They specify the stakeholder role, dataset schema, grammar constraints, paired formulation types, canonical vocabulary, output format, and number of required records. Using the same prompt, model version, and decoding settings can make the generation process highly reproducible. However, exact byte-for-byte reproduction of LLM-generated text is not always guaranteed, even when the same prompt and model version are used.

Variation may occur because of model-serving nondeterminism, decoding parameters, platform updates, hidden system instructions, or differences in post-processing. Setting deterministic parameters such as a low temperature or `temperature = 0` can reduce variation, and a fixed seed may help if the model provider supports seeded generation. Nevertheless, exact output identity cannot be assumed for all LLM services.

For this reason, this thesis treats the prompts as supporting procedural reproducibility and the released CSV files as supporting exact experimental reproducibility. The prompts show how the datasets were generated, while the final generated datasets define the fixed experimental artifacts used for parser validation, AST generation, semantic preservation evaluation, and conflict detection.

The reproducibility package should therefore include:

- prompt files
- generated CSV datasets
- model name and version
- generation date
- decoding settings, such as temperature and top-p
- grammar file
- parser implementation
- validation scripts or commands
- validation results
- any manual correction or post-processing notes

This approach allows other researchers to inspect and rerun the generation procedure while also reproducing the reported experiments exactly using the released dataset files.

## 4. Logic Representation

The formal language used in this thesis is a controlled deontic first-order logic syntax. It supports:

- Obligations: `O(...)`
- Permissions: `P(...)`
- Prohibitions: `F(...)`
- Dyadic norms: `O(p|q)`, `P(p|q)`, `F(p|q)`
- Implication-based norms: `q->O(p)`, `q->P(p)`, `q->F(p)`
- Quantifiers: `∀` and `∃`
- Predicates and terms
- Negation, conjunction, and disjunction

The revised formalization uses variables for both users and products. The variable `x` is used for users and the variable `y` is used for products or food items. Product categories are represented as predicates, such as `energyDrink(y)`, `lowSugarFood(y)`, or `glutenFreeMeal(y)`, rather than as constants. The recommendation relation includes both the recommended product and the target user:

```text
recommend(System,y,x)
```

An example natural language norm is:

```text
Children should not receive energy drink recommendations.
```

The corresponding implication-based formula is:

```text
∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))
```

The corresponding dyadic formula is:

```text
∀x.∀y.F(recommend(System,y,x)|child(x)∧energyDrink(y))
```

In these formulas, `F` represents prohibition, `recommend(System,y,x)` represents the recommendation of product `y` to user `x`, and `child(x)∧energyDrink(y)` represents the condition under which the prohibition applies.

## 5. Parser Development

### 5.1 Grammar

A parser was implemented using Lark. The grammar is designed to parse formulas from the controlled deontic first-order logic syntax. The parser supports modal operators, quantifiers, predicates, function-like terms, and logical connectives.

During development, an ambiguity occurred between constants, predicates, and function names in the first grammar version. For example, in an earlier constant-based formula:

```text
∀x.F(recommend(System,EnergyDrink)|child(x))
```

the term `System` was initially tokenized as a function name, causing the parser to expect an opening parenthesis after it. This led to an error at the comma in `recommend(System,EnergyDrink)`. Although the revised formalization now uses product variables, this debugging step was important because the grammar still needs to distinguish names structurally rather than relying on overlapping lexical categories.

The grammar was corrected by using a single `NAME` token and allowing the parser structure to determine whether a name is used as an atomic term, predicate, or function-like term. Modal operators were also given priority over generic names so that `O`, `P`, and `F` are parsed as modal operators rather than ordinary identifiers.

### 5.2 Validation

The generated datasets were validated using the parser. For each dataset, all formulas were checked for syntactic validity.

The first dataset version used constant-like product categories and one formula column. Its validation results were:

```text
User dataset:
- 100 rows
- 100 unique IDs
- 100 unique formulas
- 0 parser-invalid formulas

Food Ministry dataset:
- 100 rows
- 100 unique IDs
- 100 unique natural language norms
- 100 unique formulas
- 0 parser-invalid formulas

Food Industry dataset:
- 100 rows
- 100 unique IDs
- 100 unique natural language norms
- 100 unique formulas
- 0 parser-invalid formulas
```

These validation results show that the generated formulas are compatible with the implemented grammar and can be used for later AST generation and conflict-detection experiments.

After supervisor feedback, the formalization is being revised to use product variables, paired implication/dyadic formulas, and separate constitutive rules. The revised datasets will be revalidated after regeneration. The validation procedure remains the same, but it will be applied to both `implication_formula` and `dyadic_formula` columns.

## 6. AST Generation

After syntactic validation, the next step is to transform each parsed formula into an abstract syntax tree (AST). The parser confirms whether a formula belongs to the grammar, but the resulting parse tree is still closely tied to the grammar rules. For downstream reasoning, a cleaner structured representation is needed.

AST generation follows a two-stage process:

```text
logic formula -> Lark parse tree -> custom AST
```

For example, the implication-based formula:

```text
∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))
```

can be represented as an AST with the following structure:

```json
{
  "type": "quantifier",
  "quantifier": "forall",
  "variable": "x",
  "body": {
    "type": "quantifier",
    "quantifier": "forall",
    "variable": "y",
    "body": {
      "type": "implication",
      "condition": {
        "type": "and",
        "children": [
          {
            "type": "predicate",
            "name": "child",
            "args": ["x"]
          },
          {
            "type": "predicate",
            "name": "energyDrink",
            "args": ["y"]
          }
        ]
      },
      "consequent": {
        "type": "modal",
        "operator": "F",
        "formula": {
          "type": "predicate",
          "name": "recommend",
          "args": ["System", "y", "x"]
        }
      }
    }
  }
}
```

This representation makes the logical components of the formula explicit. The modal operator, recommendation action, and condition can be accessed directly without relying on string matching or regular expressions.

AST generation is important for conflict detection because conflicts depend on structure rather than surface text. For example, the following formulas may express a conflict:

```text
∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))
∀x.∀y.energyDrink(y)∧child(x)->O(recommend(System,y,x))
```

A string-based comparison may fail because the conditions appear in a different order. An AST-based approach can normalize conjunctions and compare the underlying structure. This makes conflict detection more systematic, explainable, and reproducible.

Although conflict detection could be attempted using direct string comparison or regular expressions, these approaches are fragile. They become unreliable when formulas include conjunction, disjunction, negation, dyadic norms, implication-based norms, or nested predicates. By contrast, ASTs provide a stable intermediate representation for later reasoning.

For this thesis, each validated formula can be converted into an AST and stored as a JSON artifact. Since each record may contain both implication-based and dyadic formulas, the AST output can preserve both structures:

```json
{
  "id": "USER001",
  "stakeholder": "User",
  "nl_norm": "Children should not receive energy drink recommendations.",
  "implication_formula": "∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))",
  "dyadic_formula": "∀x.∀y.F(recommend(System,y,x)|child(x)∧energyDrink(y))",
  "implication_ast": {},
  "dyadic_ast": {}
}
```

This creates a bridge between parser validation and conflict detection. The parser ensures that formulas are syntactically valid, while the AST representation makes them suitable for structural comparison and reasoning.

For conflict detection, both implication-based and dyadic ASTs can also be normalized into a shared internal representation:

```json
{
  "modality": "F",
  "action": "recommend(System,y,x)",
  "condition": ["child(x)", "energyDrink(y)"]
}
```

This normalization allows the conflict detector to compare norms independently of whether the original formula used implication-based or dyadic syntax.

## 7. Evaluation Design

The dataset supports several evaluation tasks:

1. Syntax validation
2. AST generation
3. Paired formulation comparison
4. Stakeholder-specific norm translation
5. Round-trip semantic preservation
6. Conflict detection between stakeholder norms
7. Comparison between dyadic and implication-based formulations

Syntax validation checks whether generated formulas can be parsed by the grammar. AST generation checks whether valid formulas can be transformed into structured representations for later reasoning. Paired formulation comparison evaluates how implication-based and dyadic formulas differ for the same natural language norm. Stakeholder-specific evaluation checks whether the formalization reflects the source stakeholder's perspective.

### 7.1 Round-Trip Semantic Preservation

Parser validation only determines whether a generated formula is syntactically valid. It does not determine whether the formula preserves the meaning of the original natural language norm. A formula may be parser-valid but semantically incorrect. For example, if the natural language norm is:

```text
Children should not receive energy drink recommendations.
```

then the following formula is syntactically valid but semantically wrong:

```text
∀x.∀y.child(x)∧energyDrink(y)->O(recommend(System,y,x))
```

The error is that the formula uses obligation rather than prohibition. To address this limitation, this thesis can include a round-trip semantic preservation evaluation. In this evaluation, each norm is translated in two directions:

```text
natural language norm -> modal FOL formula -> reconstructed natural language norm
```

The original natural language norm is then compared with the reconstructed natural language norm. If the generated formula preserved the intended meaning, the reconstructed norm should express the same stakeholder requirement, even if it uses different wording.

For example:

```text
Original natural language:
Children should not receive energy drink recommendations.

Modal FOL:
∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))

Back-translated natural language:
For every user and every product, if the user is a child and the product is an energy drink, the system is prohibited from recommending that product to that user.
```

These two natural language statements are semantically aligned. By contrast, if the modal operator is changed from `F` to `O`, the back-translation reveals that the formula has reversed the intended normative meaning.

This evaluation is relevant because the thesis studies LLM-based norm formalization rather than syntax generation alone. Round-trip evaluation complements parser validation by checking whether a syntactically valid formula also preserves the original stakeholder meaning. It also supports explainability, since formal formulas can be translated back into natural language for human inspection.

The comparison between the original and reconstructed natural language norms can be evaluated using manual semantic equivalence ratings, LLM-assisted semantic comparison, or error categories. Possible error categories include:

- wrong modality, such as obligation instead of prohibition
- missing condition
- incorrect condition
- missing recommendation action
- incorrect recommended item
- added meaning
- lost meaning
- stakeholder-perspective mismatch
- dyadic versus implication formulation mismatch

Round-trip semantic preservation should be evaluated before conflict detection. Conflict detection assumes that the formulas accurately represent the original stakeholder norms. If the translation step changes the meaning of a norm, then any detected conflict may reflect a translation error rather than a genuine stakeholder conflict.

Conflict detection is a later reasoning task. For example, a User norm may prohibit recommending a food item under a condition, while an Industry norm may obligate recommending that same item under a compatible condition. Detecting such conflicts requires syntactic validity, structured logical representations, and normalization into a common format such as modality, action, and condition.

## 8. Next Writing Tasks

The following sections still need to be developed:

- Literature review on recommender systems, normative systems, deontic logic, and LLM-based formalization
- Detailed grammar explanation
- AST design and examples
- Conflict detection method
- Experimental setup
- Results tables
- Discussion of limitations
- Conclusion
