# Leveraging LLMs for Stakeholder Norm Formalization in DJ4ME

## Working Thesis Draft: DJ4ME-Oriented Version

This document is a second working thesis draft. It reframes the work around the DJ4ME project, where stakeholder norms are represented for use in machine-ethics dialogue, argumentation, explanation, and conflict analysis. The food recommender system is treated as a case study rather than as the whole research context.

## 1. Introduction

Autonomous artificial agents increasingly operate in domains where their decisions affect the interests, wellbeing, rights, and freedoms of multiple stakeholders. In such settings, decision-making cannot be reduced to technical optimization alone. Agents may face situations in which users, regulators, manufacturers, service providers, and the broader public hold different and sometimes conflicting normative expectations. This raises a central question for machine ethics: whose norms should an autonomous agent follow, and how can its decision be justified to the affected stakeholders?

The DJ4ME project, *A DJ for Machine Ethics: the Dialogue Jiminy*, addresses this challenge by investigating how stakeholder views can be represented in agent decision-making through dialogue and argumentation. Since stakeholders cannot always be consulted in real time, their views may be represented by avatars that use norms to construct arguments and provide moral recommendations to the agent. For such a system to work, stakeholder norms expressed in natural language must be translated into formal representations that can be validated, compared, and used for reasoning.

This thesis contributes to that goal by studying LLM-based norm formalization for an agent-based normative food recommender system used as a case study. Food recommendation is a suitable domain because recommendations may involve several competing normative concerns, including user preferences, allergies, medical conditions, religious dietary requirements, public-health regulation, product safety, and commercial interests. A recommendation that is acceptable from one stakeholder perspective may be inappropriate or prohibited from another.

The central task of this thesis is to translate stakeholder norms from natural language into modal first-order logic formulas. These formulas are intended to represent obligations, permissions, and prohibitions concerning recommendation actions. The work focuses on three stakeholder perspectives: users, a food ministry, and the food industry. For each stakeholder, natural language norms are formalized using a controlled grammar, validated with a parser, transformed into abstract syntax tree representations, and prepared for conflict detection.

A key methodological issue addressed in the thesis is the representation of conditional norms. Conditional norms may be expressed using implication-based monadic formulas, such as `X->O(Y)`, or dyadic formulas, such as `O(Y|X)`. These representations are not assumed to be semantically equivalent. Instead, this thesis treats them as alternative formalization strategies and investigates how they affect validation, AST generation, semantic preservation, and conflict detection.

The thesis also considers the semantic adequacy of the formalizations. Parser validation can determine whether a formula is syntactically valid, but it cannot determine whether the formula preserves the meaning of the original natural language norm. Therefore, the thesis includes a round-trip evaluation in which formalized norms are translated back into natural language and compared with the original norm. This supports evaluation of whether LLM-generated formulas preserve stakeholder meaning.

Overall, the thesis aims to develop and evaluate a reproducible pipeline for stakeholder norm formalization in the context of DJ4ME. The pipeline connects natural language stakeholder norms, modal first-order logic, parser validation, AST generation, semantic preservation, and conflict detection. By doing so, the work contributes to the broader goal of enabling autonomous agents to reason with stakeholder norms and to support more transparent and explainable machine-ethical decision-making.

## 2. Research Context

### 2.1 DJ4ME And Stakeholder Norms

DJ4ME studies machine ethics for autonomous agents whose decisions may affect multiple stakeholders. A central idea is that stakeholders can be represented by avatars, and these avatars can use norms to build arguments and participate in dialogue about what an agent should do.

This thesis focuses on the upstream formalization step needed for such a system. Stakeholders often express norms in natural language, but dialogue, argumentation, parser validation, and conflict detection require more structured representations. The thesis therefore investigates how LLMs can translate stakeholder-expressed norms into a controlled modal first-order logic language.

### 2.2 Food Recommendation As Case Study

The case study is a normative food recommender system. The recommender is treated as an agent whose recommendations may be evaluated by different stakeholder avatars:

- User
- Food Ministry
- Food Industry

Users may express personal, medical, religious, ethical, budgetary, and taste-related norms. A Food Ministry may express public-health, safety, labeling, and regulatory norms. Food Industry actors may express product-placement, market-access, certification, availability, and compliance-related norms.

This case study is useful because conflicts can naturally arise. A user may prohibit recommending a certain product, while an industry stakeholder may promote it, or a regulator may restrict it under certain conditions.

## 3. Research Questions

The main research question is:

```text
How can large language models support the translation, validation, and analysis of stakeholder norms for DJ4ME-style agent-based normative recommender systems?
```

The thesis can be guided by the following sub-questions:

```text
RQ1: How accurately can LLMs translate stakeholder norms from natural language into modal first-order logic?

RQ2: To what extent do generated modal first-order logic formulas satisfy the syntax of a controlled grammar?

RQ3: To what extent do generated formulas preserve the meaning of the original natural language norm under round-trip translation?

RQ4: How do implication-based monadic formulations and dyadic formulations compare in terms of syntax validity, AST structure, semantic preservation, and suitability for conflict detection?

RQ5: How can AST-based and normalized representations support detection of conflicts between stakeholder norms?
```

## 4. Dataset Construction

### 4.1 Dataset Purpose

The dataset is a stakeholder norm translation dataset. It is not a recommendation dataset. Each record contains a natural language norm and formal representations of that norm. The purpose is to support evaluation of LLM-based norm formalization and later conflict detection.

The dataset supports the following DJ4ME-relevant pipeline:

```text
stakeholder natural language norm
-> avatar-readable formal norm
-> parser validation
-> AST generation
-> normalized norm representation
-> conflict detection
-> explanation or dialogue support
```

### 4.2 Revised Main Dataset Schema

The revised main stakeholder dataset uses paired formalizations:

```text
id
stakeholder
nl_norm
implication_formula
dyadic_formula
norm_type
```

The `implication_formula` column contains an implication-based monadic formulation such as:

```text
∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))
```

The `dyadic_formula` column contains a dyadic formulation of the same norm:

```text
∀x.∀y.F(recommend(System,y,x)|child(x)∧energyDrink(y))
```

This paired structure makes it possible to compare the two formalization strategies for the same natural language norm.

### 4.3 Stakeholders

Three stakeholder perspectives are represented:

- User: personal needs, allergies, medical restrictions, religious diets, ethical preferences, taste preferences, and avoidance preferences.
- Food Ministry: public health, vulnerable population protection, nutrition thresholds, allergen disclosure, labeling compliance, and restricted products.
- Food Industry: sponsored products, certified products, availability, seasonal products, market segmentation, premium products, and compliance constraints.

### 4.4 Product Variables And Predicates

The revised design avoids treating food categories as constants. A term such as `GlutenFreeMeal` should not represent an entire class of products. Instead, product categories are represented as predicates over product variables.

For example, instead of:

```text
∀x.requiresGlutenFree(x)->P(recommend(System,GlutenFreeMeal))
```

the revised formalization uses:

```text
∀x.∀y.requiresGlutenFree(x)∧glutenFreeMeal(y)∧certifiedGlutenFree(y)->P(recommend(System,y,x))
```

Here, `x` ranges over users and `y` ranges over products. The recommendation relation `recommend(System,y,x)` states that the system recommends product `y` to user `x`.

The truth of predicates such as `glutenFreeMeal(y)` or `certifiedGlutenFree(y)` would be supplied by a domain interpretation, such as a product catalog, food ontology, or knowledge base. The current thesis focuses on norm translation and structural analysis rather than building a complete product database.

### 4.5 Constitutive Rules

Some domain knowledge is better represented through constitutive rules. Constitutive rules define classifications, while normative rules express obligations, permissions, or prohibitions.

For example:

```text
∀y.shellfishMeal(y)->nonVegan(y)
```

This can support a general norm:

```text
∀x.∀y.vegan(x)∧nonVegan(y)->F(recommend(System,y,x))
```

In the revised design, constitutive rules are stored separately from the main stakeholder norm dataset. This prevents the main dataset from mixing normative rules with background classification rules.

## 5. Logic Representation

The target language is a controlled modal first-order logic syntax supporting:

- obligations: `O(...)`
- permissions: `P(...)`
- prohibitions: `F(...)`
- implication-based norms: `X->O(Y)`, `X->P(Y)`, `X->F(Y)`
- dyadic norms: `O(Y|X)`, `P(Y|X)`, `F(Y|X)`
- universal and existential quantification
- predicates, terms, conjunction, disjunction, and negation

The preferred recommendation relation is:

```text
recommend(System,y,x)
```

where `y` is the product being recommended and `x` is the target user.

Example natural language norm:

```text
Children should not receive energy drink recommendations.
```

Implication-based formulation:

```text
∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))
```

Dyadic formulation:

```text
∀x.∀y.F(recommend(System,y,x)|child(x)∧energyDrink(y))
```

## 6. Parser Validation

A parser is used to validate whether generated formulas conform to the fixed grammar. Parser validation is important because LLMs may produce formulas that look plausible but are not syntactically valid under the intended formal language.

The earlier grammar was corrected to reduce lexical ambiguity between constants, predicates, and function names. The revised formalization must also support:

- multiple quantified variables, such as `∀x.∀y.`
- product predicates, such as `energyDrink(y)`
- recommendation relations with user and product arguments, such as `recommend(System,y,x)`
- both implication-based and dyadic modal formulas

The revised datasets should be validated by checking both formula columns:

```text
implication_formula
dyadic_formula
```

## 7. AST Generation And Normalization

After parser validation, formulas are transformed into ASTs. ASTs make the structure of the formula explicit and allow the system to access components such as modality, action, condition, quantifier, and predicates.

For example:

```text
∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))
```

can be normalized into:

```json
{
  "modality": "F",
  "action": "recommend(System,y,x)",
  "condition": ["child(x)", "energyDrink(y)"]
}
```

The normalized representation is important because both implication-based and dyadic formulas can be mapped into the same operational form. This makes conflict detection easier and reduces the chance of missing conflicts because two equivalent-looking norms were written in different formalization styles.

## 8. Round-Trip Semantic Preservation

Parser validation only checks syntax. It does not check whether the generated formula preserves the meaning of the original natural language norm.

To evaluate semantic preservation, the thesis includes round-trip translation:

```text
natural language norm
-> modal first-order logic
-> reconstructed natural language norm
```

For example:

```text
Original:
Children should not receive energy drink recommendations.

Formula:
∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))

Back translation:
For every user and every product, if the user is a child and the product is an energy drink, the system is prohibited from recommending that product to that user.
```

The original and reconstructed natural language statements can then be compared for semantic equivalence.

## 9. Conflict Detection

Conflict detection is one of the downstream goals of the formalization pipeline. In the DJ4ME context, conflicts can be understood as potential points of disagreement between stakeholder avatars.

A simple direct conflict can be detected when two norms have:

- the same or compatible recommendation action
- the same or overlapping condition
- opposing modalities, such as `O` versus `F`, or `P` versus `F`

Example:

```text
User:
∀x.∀y.vegan(x)∧nonVegan(y)->F(recommend(System,y,x))

Food Industry:
∀x.∀y.eligible(x)∧sponsored(y)->O(recommend(System,y,x))
```

If a user is vegan and eligible, and a sponsored product is also non-vegan, the two norms may conflict. Constitutive rules can help identify such cases by connecting specific product categories to broader classes.

The thesis can compare:

```text
LLM-based conflict detection on natural language norms
```

with:

```text
logic-based conflict detection on formalized and normalized norms
```

This comparison directly follows the project goal of investigating conflict detection from both natural language and formal representations.

## 10. Reproducibility

The prompts document the procedure used to generate the datasets. They specify the stakeholder role, dataset schema, grammar constraints, paired formalization types, canonical vocabulary, output format, and number of required records.

However, exact byte-for-byte reproduction of LLM-generated text is not always guaranteed, even with the same model version and prompt. Therefore, the prompts support procedural reproducibility, while the released CSV datasets support exact experimental reproducibility.

The reproducibility package should include:

- prompt files
- generated CSV datasets
- grammar file
- parser implementation
- AST generation scripts
- validation results
- model name and version
- generation date
- decoding settings
- post-processing notes

## 11. Planned Evaluation

The thesis can evaluate the pipeline using the following criteria:

1. Syntax validity of generated formulas.
2. Correct use of user and product variables.
3. Correct representation of product categories as predicates.
4. Semantic preservation through round-trip translation.
5. AST generation success.
6. Normalization success for implication and dyadic formulas.
7. Conflict detection on normalized formal norms.
8. Comparison between LLM-based conflict detection on natural language and logic-based conflict detection on formal norms.

## 12. Next Steps

The immediate next steps are:

- revise prompts to use the new paired dataset schema
- regenerate a small pilot dataset using the revised formalization
- update the grammar if needed for `∀x.∀y.` and `recommend(System,y,x)`
- validate both formula columns
- generate ASTs for both formula types
- implement normalization into modality, action, and condition
- design a small conflict-detection experiment
- design a round-trip semantic preservation evaluation

