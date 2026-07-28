Faculty of Science, Technology and Communication

Leveraging LLMs for Agent-Based Normative Recommender Systems

A Pipeline for Stakeholder Norm Translation, Validation, and Formulation Comparison

Thesis Submitted in Partial Fulfillment of the Requirements for the Degree of Master in Information and Computer Sciences

Author: Nabila Waheed

Supervisor: [Supervisor name]

Advisor: [Advisor name]

Reviewer: [Reviewer name]

Date: Working draft, 2026

# Abstract

Autonomous recommender systems increasingly operate in domains where recommendations are not merely matters of preference optimization, but also involve ethical, legal, health-related, and stakeholder-specific constraints. In food recommendation, for example, a system may need to respect user allergies, religious dietary requirements, public-health restrictions, product-safety rules, and commercial objectives. These requirements are often expressed in natural language, while formal reasoning, parser validation, argumentation, dialogue, and explanation require structured representations.

This thesis investigates how large language models can support the formalization of stakeholder norms for an agent-based normative recommender system. The work is situated in the context of DJ4ME, where stakeholder views may be represented by avatars that reason with norms and participate in machine-ethics dialogue. The thesis translates stakeholder norms into a controlled modal/deontic first-order logic syntax that supports obligations, permissions, prohibitions, implication-based monadic conditional formulations, and dyadic conditional formulations. Three stakeholder perspectives are considered: User, Food Ministry, and Food Industry.

The current implementation constructs a norm translation dataset rather than a recommendation dataset. Each natural-language norm is paired with both an implication-based monadic formulation and a dyadic formulation. This design supports comparison between formalization strategies rather than treating them as interchangeable. Product categories are modeled as predicates over product variables, and the recommendation relation is represented as recommend(System,y,x), where y is the product and x is the target user. Constitutive rules, such as category classifications, are stored separately from stakeholder norms as background domain knowledge.

The pipeline includes grammar-based validation, abstract syntax tree generation, normalized formula representations, and round-trip semantic preservation checks. The current validated dataset contains 350 records and 650 formal formulas with zero parser validation errors. It also produces 350 AST records and 600 round-trip backtranslation rows. The thesis contributes a structured dataset design and implementation pipeline for evaluating LLM-based norm formalization and preparing stakeholder norms for later use in DJ4ME-style dialogue, explanation, and reasoning components.

Keywords: large language models; deontic logic; first-order logic; normative recommender systems; stakeholder norms; grammar validation; abstract syntax trees; round-trip evaluation

# List of Tables

Table 3.1 Dataset schemas and record counts
Table 3.2 Main validation checks
Table 4.1 Current validation results
Table 4.2 Round-trip automatic score interpretation

# List of Figures

Figure 3.1 Overview of the norm formalization pipeline
Figure 3.2 Formula-to-AST normalization flow
Figure 4.1 Round-trip semantic preservation workflow
Figure 4.2 Planned downstream use in DJ4ME

# Table of Contents

1 Introduction
    1.1 Background and Motivation
    1.2 Problem Statement
    1.3 Research Questions
    1.4 Contributions
    1.5 Thesis Structure

2 Literature Review
    2.1 Large Language Models and Formalization
    2.2 Natural Language to Logic Translation
    2.3 Deontic Logic and Normative Agents
    2.4 Multi-Stakeholder Recommender Systems
    2.5 Food Recommendation and Constraint-Aware Systems
    2.6 Research Gap

3 Methodology
    3.1 Research Design
    3.2 Dataset Construction
    3.3 Logic Grammar and Formalization Conventions
    3.4 Parser Validation
    3.5 AST Generation and Normalization
    3.6 Round-Trip Semantic Preservation
    3.7 LLM Comparison and Human Semantic Review
    3.8 Scope Boundary and Downstream DJ4ME Use

4 Results and Discussion
    4.1 Dataset Outputs
    4.2 Parser Validation Results
    4.3 AST and Round-Trip Outputs
    4.4 Claude Comparison Results
    4.5 Discussion

5 Conclusion and Future Work
    5.1 Contributions
    5.2 Limitations
    5.3 Future Work

# Chapter 1: Introduction

## 1.1 Background and Motivation

Artificial intelligence systems are increasingly deployed in settings where their outputs influence the choices, wellbeing, and rights of human users. Recommender systems are a central example of this development. They shape what users see, consume, buy, and consider relevant. In many applications, recommendation quality is usually discussed in terms of accuracy, personalization, engagement, or utility. However, when recommendations concern sensitive domains such as food, health, wellbeing, or lifestyle, purely preference-based optimization is insufficient. A recommendation can be technically relevant while still being inappropriate, unsafe, unfair, or normatively unacceptable.

Food recommendation provides a useful case study because the domain naturally contains many kinds of normative constraints. A user may require halal, kosher, vegan, gluten-free, lactose-free, low-sugar, or low-salt food. A child should not receive recommendations for energy drinks or age-restricted products. A person with an allergy should not receive food containing a harmful ingredient. A food ministry may require labeling, safety warnings, and protection of vulnerable users. Food industry actors may want to promote certified, sponsored, seasonal, or available products, while still respecting safety and compliance constraints. These concerns cannot be reduced to a single preference score.

The DJ4ME project, A DJ for Machine Ethics: the Dialogue Jiminy, motivates this thesis. DJ4ME investigates how autonomous agents can make ethically relevant decisions by representing stakeholder perspectives through dialogue and argumentation. The project builds on the idea that affected stakeholders may be represented by avatars embedded in or connected to the agent. These avatars can hold norms, make arguments, and participate in dialogue about what the agent should do. In contrast to a purely automatic moral advisor that aggregates stakeholder norms internally, Dialogue Jiminy aims to preserve stakeholder autonomy by allowing avatars to participate in persuasion dialogue.

The DJ4ME proposal identifies a natural-language interface as one of the core requirements for such a system. This interface is expected to support both norm mining and explanation synthesis. Norm mining and norm formalisation concern the transformation of informal stakeholder norms into formal rules usable by avatars. Explanation synthesis concerns the reverse direction: making formal recommendations or dialogues understandable in plain natural language. This thesis focuses on the first part of that interface: translating stakeholder norms from natural language into a controlled modal/deontic first-order logic syntax that supports obligations, permissions, prohibitions, implication-based monadic conditional formulations, and dyadic conditional formulations.

Large language models are promising for this task because they are capable of interpreting natural-language rules and producing structured symbolic expressions. At the same time, LLMs are not guaranteed to produce valid formulas or semantically faithful translations. They may invent predicates, mix notation styles, omit variables, or produce formulas that look plausible but cannot be parsed. This thesis therefore studies LLM-based norm formalization as part of a controlled pipeline that combines natural-language generation, fixed grammar validation, AST generation, round-trip semantic checks, LLM comparison, and human semantic review.

## 1.2 Problem Statement

Stakeholder norms are often available in natural language, but agent-based normative reasoning and dialogue require formal representations. The central problem is how to translate stakeholder norms into formulas in a controlled modal/deontic first-order logic syntax that supports obligations, permissions, prohibitions, implication-based monadic conditional formulations, and dyadic conditional formulations, while keeping the formulas syntactically valid, semantically meaningful, and reusable by downstream DJ4ME components. This problem is made more difficult by the fact that conditional norms can be represented in different formal styles. In particular, implication-based monadic norms and dyadic norms have different semantic interpretations and should not be treated as interchangeable.

A second modeling problem concerns product categories. Early versions of the dataset used expressions such as recommend(System,EnergyDrink), where a category such as EnergyDrink was treated as a constant. This is problematic because a constant denotes a particular object in a model rather than a class of products. The revised design instead quantifies over product variables and represents categories as predicates, such as energyDrink(y). This makes the formalization more suitable for a single domain model containing many products.

A third problem concerns redundancy. Some norms should not be repeated for every specific food category if broader constitutive classifications can be used. For example, shellfish meals, meat meals, dairy meals, and egg meals can be classified as non-vegan through background rules. A general user norm can then prohibit recommendations of non-vegan products to vegan users. The thesis therefore separates normative stakeholder rules from constitutive domain rules.

## 1.3 Research Questions

The main research question is:

How can large language models support the translation, validation, and analysis of stakeholder norms for agent-based normative recommender systems?

The thesis is guided by the following sub-questions:

1. How accurately can LLMs translate stakeholder norms from natural language into formulas in a controlled modal/deontic first-order logic syntax?

1. To what extent do generated formulas satisfy the syntax of a controlled grammar?

1. To what extent do generated formulas preserve the meaning of the original natural-language norm under round-trip translation?

1. How do implication-based monadic formulations and dyadic formulations compare in terms of syntax validity, AST structure, and semantic preservation?

1. How reliable is automatic round-trip evaluation when compared with human semantic review?

The fourth sub-question is motivated by the fact that conditional stakeholder norms can be formalized in more than one plausible way. For example, a norm such as "children should not receive energy drink recommendations" can be represented as an implication-based formula, where the condition implies a monadic prohibition, or as a dyadic formula, where the prohibition is conditional on the relevant user and product properties. The thesis does not assume that these two forms are semantically identical. Instead, it treats them as alternative formalization strategies whose behavior can be compared under controlled conditions.

## 1.4 Contributions

- A revised stakeholder norm dataset design for User, Food Ministry, and Food Industry perspectives.

- A paired formalization strategy in which each natural-language norm has both implication-based and dyadic formulas.

- A corrected modeling convention that represents product categories as predicates over quantified product variables.

- A separate constitutive-rule dataset for background domain classifications.

- A reproducible parser-validation and AST-generation pipeline.

- A round-trip semantic preservation workflow with automatic triage scores and human-evaluation results.

- A comparison between a baseline LLM-generated dataset and a Claude-generated dataset produced from the same prompt structure.

## 1.5 Thesis Structure

Chapter 2 reviews related work on DJ4ME, LLM-based formalization, natural-language-to-logic translation, deontic logic, normative agents, multi-stakeholder recommender systems, and food recommendation. Chapter 3 presents the methodology, including dataset construction, grammar design, parser validation, AST generation, round-trip evaluation, LLM comparison, and human semantic review. Chapter 4 reports current implementation results and discusses their implications. Chapter 5 concludes the thesis by summarizing contributions, limitations, and future work.

# Chapter 2: Literature Review

## 2.1 DJ4ME and Machine Ethics

The DJ4ME project provides the research context for this thesis. It studies machine ethics for autonomous agents whose decisions may affect multiple stakeholders. The proposal connects machine ethics with deontic logic, normative systems, formal argumentation, argumentation as dialogue, and machine learning. Its central architectural idea is that stakeholders can be represented by avatars. These avatars can hold norms and participate in reasoning or dialogue about what an autonomous agent should do.

DJ4ME builds on the Autonomous Jiminy architecture, where stakeholder norms can be combined into arguments in order to identify moral dilemmas and recommend actions to the agent. The Dialogue Jiminy extension shifts the focus toward persuasion dialogue between stakeholder avatars. This is important because it gives stakeholders more control over how their norms are used in the moral recommendation process.

The proposal identifies a natural-language interface as a key part of the project. This interface includes norm mining, norm formalisation, and explanation synthesis. Norm formalisation is the part most relevant to this thesis: informal stakeholder norms must be converted into formal rules that can be validated and used by avatars or reasoning components. The thesis contributes to this upstream formalisation task by constructing and evaluating a pipeline for translating stakeholder food-recommendation norms into formulas in a controlled modal/deontic first-order logic syntax.

## 2.2 Large Language Models and Formalization

Large language models have demonstrated strong abilities in natural-language understanding, text generation, summarization, and code-like symbolic output. These capabilities make them attractive for translating informal requirements or norms into formal languages. However, LLMs also introduce risks. They may produce syntactically invalid expressions, hallucinate predicates, collapse distinctions that matter semantically, or generate outputs that are fluent but not faithful to the source. In formalization tasks, these errors are especially important because small notation changes can alter the meaning of a formula.

For this thesis, LLMs are not treated as standalone reasoners. Instead, they are treated as components in a hybrid pipeline. The LLM can assist in producing candidate formalizations, but the output must be checked by a grammar and parser before it is used for reasoning. This follows a broader direction in neurosymbolic AI: using language models for flexible linguistic interpretation while relying on formal tools for validation and structured reasoning.

## 2.3 Natural Language to Logic Translation

Work on natural-language-to-first-order-logic translation is directly relevant to this thesis. The LOGICLLAMA line of work, for example, studies how LLMs can translate natural language into first-order logic and emphasizes dataset generation, prompt design, grammar verification, and correction strategies. Such work shows that LLMs can be useful for formal translation tasks, but also that generated formulas require validation and that silver-label datasets should be handled carefully.

FOLIO is another relevant reference because it provides natural-language statements paired with first-order logic annotations. It demonstrates the value of formal annotations for reasoning tasks and highlights the importance of carefully checked logical representations. However, FOLIO focuses on general first-order logic rather than deontic or modal norms.

This thesis differs from standard NL-to-FOL work by focusing on a controlled modal/deontic first-order logic syntax for stakeholder norms. The target formulas contain obligations, permissions, prohibitions, implication-based conditional formulas, and dyadic conditional formulas. The immediate goal is not to build a complete moral dialogue system, but to evaluate whether LLM-generated stakeholder norms can be expressed in a controlled formal language with valid syntax and preserved meaning.

## 2.4 Deontic Logic and Normative Agents

Deontic logic provides formal tools for representing normative concepts such as obligation, permission, and prohibition. In this thesis, the operators O, P, and F are used to represent these modalities. Conditional norms can be represented using implication-based formulas, such as X->O(Y), or dyadic formulas, such as O(Y|X). These forms are not treated as semantically identical. The thesis therefore keeps both forms paired for the same natural-language norm in order to support comparison.

Normative agent research is also relevant because autonomous agents may need to reason about what they are permitted, required, or forbidden to do. Norm conflicts are a central challenge in this area. A system may face one norm requiring an action and another norm prohibiting the same action under overlapping conditions. Resolving such conflicts may require priorities, defeasible reasoning, or argumentation semantics. In this thesis, conflict handling is treated as a downstream DJ4ME use case rather than as an implemented component. The implemented focus is the formalisation and evaluation of the norms that such a component would later require.

## 2.5 Multi-Stakeholder Recommender Systems

Multi-stakeholder recommender systems recognize that recommendations affect more than one party. A recommendation may benefit a user, a provider, a platform, a regulator, or a broader public interest. Research on multi-stakeholder recommendation and multi-sided fairness shows that recommender systems may need to balance competing objectives and constraints across different actors.

The stakeholder framing is central to this thesis. User norms represent individual needs and constraints, Food Ministry norms represent public-health and regulatory concerns, and Food Industry norms represent commercial and product-placement objectives. The thesis formalizes these perspectives separately so that downstream DJ4ME components could later compare stakeholder positions in argumentation or dialogue.

## 2.6 Food Recommendation and Constraint-Aware Systems

Food recommendation is often discussed in relation to personalization, nutrition, health, dietary constraints, and recipe retrieval. Constraint-aware food recommendation systems and food knowledge graphs show that food recommendations may depend on structured information about ingredients, dietary labels, allergens, and user requirements. This thesis does not build a complete food knowledge graph, but it uses a similar idea at the logical level: predicates such as glutenFreeMeal(y), contains(y,Nuts), highSugarProduct(y), and certifiedHalal(y) represent product properties that a domain model could later interpret.

The food domain is therefore suitable as a case study for normative recommendation. It contains personal preferences, safety constraints, religious requirements, medical needs, regulatory obligations, and commercial interests. These properties make it a rich setting for studying stakeholder norm formalization.

## 2.7 Research Gap

Existing work studies LLM-based logic translation, normative agents, deontic reasoning, multi-stakeholder recommendation, and food recommendation. However, there is limited work combining these directions into a reproducible pipeline for translating stakeholder food-recommendation norms into formulas in a controlled modal/deontic first-order logic syntax that supports obligations, permissions, prohibitions, implication-based monadic conditional formulations, and dyadic conditional formulations; validating those formulas with a parser; generating ASTs; comparing LLM-generated datasets; and evaluating round-trip semantic preservation with human review. This thesis addresses that gap by building and evaluating such a pipeline in a focused case study aligned with the DJ4ME language-interface objective.

# Chapter 3: Methodology

## 3.1 Research Design

The research follows an implementation-oriented design. The objective is to construct a reproducible pipeline that takes stakeholder norms in natural language and produces validated formulas in a controlled modal/deontic first-order logic syntax that supports obligations, permissions, prohibitions, implication-based monadic conditional formulations, and dyadic conditional formulations. These formulas are suitable for AST generation, semantic checking, LLM comparison, and later use by DJ4ME components. The dataset is not a recommendation dataset, and the pipeline is not intended to produce food recommendations directly. Instead, it supports the upstream language-interface task of formalizing norms that could later be used by stakeholder avatars or normative reasoning components.

The work is structured around three stakeholder perspectives: User, Food Ministry, and Food Industry. For each stakeholder, norms are expressed in natural language and formalized using two alternative conditional structures. The resulting formulas are validated against a fixed grammar, parsed into ASTs, normalized into comparable structures, and used for round-trip backtranslation.

Figure 3.1 gives the conceptual pipeline:

natural-language stakeholder norm -> controlled modal/deontic FOL syntax -> parser validation -> AST -> normalized norm -> round-trip evaluation -> human semantic review

## 3.2 Dataset Construction

The dataset is a norm translation dataset. Each stakeholder record contains a natural-language norm and two formal representations of that norm. The revised stakeholder schema is shown in Table 3.1. The key design decision is that implication-based and dyadic formulas are paired within the same record rather than stored as unrelated records. This allows the thesis to compare the two formalization strategies for the same natural-language content.

The original motivation for using both formulations was to avoid making a premature theoretical commitment to one representation of conditional norms. Implication-based formulas and dyadic deontic formulas are both common ways of expressing conditional normative statements, but they differ in how the condition is placed. In an implication-based formulation, the condition is outside the modal operator, as in X->O(Y). In a dyadic formulation, the condition is part of the modal expression itself, as in O(Y|X). Since these forms have different logical interpretations, the dataset pairs them for each natural-language norm instead of treating them as interchangeable duplicates.

| Dataset | Schema | Current size |
| --- | --- | --- |
| Stakeholder norms | id, stakeholder, nl_norm, implication_formula, dyadic_formula, norm_type | 300 records |
| Constitutive rules | id, scope, nl_rule, logic_rule, category | 50 records |
| Total | Main norms plus background rules | 350 records |

The User dataset contains norms concerning dietary requirements, allergies, medical conditions, religious diets, ethical preferences, affordability, taste, and avoidance constraints. The Food Ministry dataset contains norms related to public health, vulnerable users, nutrition thresholds, safety warnings, labeling, approval, and restricted products. The Food Industry dataset contains norms related to sponsored products, certified products, market placement, availability, seasonal products, premium users, and compliance constraints.

### 3.2.1 Product Variables and Predicates

Product categories are modeled as predicates over product variables rather than constants. This means that a category such as gluten-free meal is represented as glutenFreeMeal(y), where y ranges over products. The recommendation relation is represented as recommend(System,y,x), where y is the product and x is the target user. This design avoids treating product categories as single objects and makes the formulas more suitable for interpretation over a product domain.

∀x.∀y.requiresGlutenFree(x)∧glutenFreeMeal(y)∧certifiedGlutenFree(y)->P(recommend(System,y,x))

### 3.2.2 Constitutive Rules

Constitutive rules are separated from stakeholder norms. They define background classifications rather than obligations, permissions, or prohibitions. For example, shellfishMeal(y)->nonVegan(y) states that shellfish meals count as non-vegan products. Such rules can reduce redundancy because several specific food categories can be mapped to broader classes used by stakeholder norms.

∀y.shellfishMeal(y)->nonVegan(y)

## 3.3 Logic Grammar and Formalization Conventions

The target language is a controlled modal/deontic first-order logic syntax. It supports universal and existential quantifiers, predicates, terms, conjunction, disjunction, negation, implication, and modal operators for obligation, permission, and prohibition. The grammar is implemented in Lark and stored in grammar/grammar.lark. All formulas in the revised datasets are validated against this grammar.

- O(...) represents obligation.

- P(...) represents permission.

- F(...) represents prohibition.

- X->O(Y), X->P(Y), and X->F(Y) represent implication-based monadic conditional norms.

- O(Y|X), P(Y|X), and F(Y|X) represent dyadic conditional norms.

Example formalizations for the same natural-language norm are:

NL: Children should not receive energy drink recommendations.
Implication: ∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x))
Dyadic: ∀x.∀y.F(recommend(System,y,x)|child(x)∧energyDrink(y))

This design is based on several assumptions. First, the same natural-language conditional norm can often be given both an implication-based and a dyadic formalization. Second, the two formulations are not assumed to be logically equivalent; they are treated as rival or alternative representations of conditional normativity. Third, LLMs may handle the two forms differently, either syntactically or semantically. Fourth, ASTs can expose structural differences that are not visible from parser validity alone. Finally, round-trip backtranslation can provide an approximate test of whether the practical meaning of the norm is preserved in each formulation.

## 3.4 Parser Validation

Parser validation checks whether generated formulas satisfy the fixed grammar and the revised modeling conventions. It is necessary because LLM-generated formulas may look plausible while containing syntax errors, missing variables, inconsistent arity, or old constant-based recommendation structures. The validation script checks both formula columns in each stakeholder dataset and the logic_rule column in the constitutive rules dataset.

| Validation check | Purpose |
| --- | --- |
| Schema validation | Confirms that each CSV has the expected columns. |
| Parser validation | Confirms that each formula can be parsed by the fixed grammar. |
| Formula-type markers | Checks that implication formulas contain -> and dyadic formulas contain \|. |
| Recommendation arity | Checks that stakeholder formulas use recommend(System,y,x). |
| Quantifier pattern | Checks stakeholder formulas start with ∀x.∀y. and constitutive rules start with ∀y. |
| Uniqueness | Flags duplicate ids, natural-language norms, or formulas. |
| Old-style guard | Rejects previous category-as-constant recommendation forms. |

## 3.5 AST Generation and Normalization

After validation, formulas are parsed into abstract syntax trees. The AST makes the structure of a formula explicit, which is important for later reasoning. Instead of searching formula strings directly, the system can access components such as quantifiers, modality, action, and condition. The script generate_asts.py creates JSON AST outputs for the three stakeholder datasets and the constitutive rules.

For example, an implication-based prohibition can be normalized as:

{
  "form": "implication",
  "modality": "F",
  "action": "recommend(System,y,x)",
  "condition": ["child(x)", "energyDrink(y)"]
}

This normalized representation is useful because both implication-based and dyadic formulas can be represented through common fields. This makes it easier to compare whether the two formalisation strategies preserve the same modality, action, and condition structure for the same natural-language norm.

## 3.6 Round-Trip Semantic Preservation

Parser validation is necessary but insufficient. It checks whether a formula is syntactically valid, but it does not prove that the formula preserves the meaning of the original natural-language norm. To address this, the thesis includes a round-trip semantic preservation step. In this step, formal formulas are converted into normalized ASTs and then backtranslated into controlled natural language. The original natural-language norm and the backtranslated statement can then be compared.

original NL -> formula -> AST -> backtranslated NL -> automatic score + human review

The automatic evaluation assigns a preliminary score. A score of 2 indicates that modality and key concepts appear preserved. A score of 1 indicates partial preservation or modality uncertainty. A score of 0 indicates a possible semantic mismatch requiring human review. The evaluated output file also includes blank columns for human semantic score, human error type, and human notes.

| Score | Meaning | Use in thesis |
| --- | --- | --- |
| 2 | Strong automatic agreement | Likely semantically preserved, still sample-check manually. |
| 1 | Partial agreement | Requires review of missing or weakened concepts. |
| 0 | Possible mismatch | Priority candidate for human evaluation. |

## 3.7 LLM Comparison and Human Semantic Review

To test whether the pipeline is model-specific or more generally useful, the thesis compares two LLM-generated datasets produced from the same prompt structure. The baseline dataset was generated in the working pipeline, while a second dataset was generated with Claude Opus 4.8 using high effort in fresh chats. The Claude stakeholder datasets were generated on 2026-06-28, and the Claude constitutive rules were generated on 2026-07-03. No manual edits were made to the Claude outputs before validation. This allows comparison of parser validity, formula structure, predicate vocabulary, norm-type distribution, and round-trip preservation.

Human semantic review is used because automatic evaluation cannot fully determine whether a formula preserves the meaning of the original natural-language norm. In the current evaluation, a human reviewer inspected a selected subset of round-trip rows, including all rows that the automatic evaluator scored as 0 or 1 and additional quality-control rows from score-2 cases. The reviewer assigned human semantic scores and error categories.

## 3.8 Scope Boundary and Downstream DJ4ME Use

Conflict detection is not implemented as part of this thesis. It remains a downstream use case for DJ4ME. The ASTs and constitutive rules are nevertheless useful because they make the formalized norms easier to reuse in future argumentation, dialogue, or conflict-analysis components.

# Chapter 4: Results and Discussion

## 4.1 Dataset Outputs

The current revised implementation produces three stakeholder datasets and one constitutive-rule dataset. Each stakeholder dataset contains 100 records, and each record contains two formulas. The constitutive-rule dataset contains 50 background rules. This produces 350 total records and 650 formulas for parser validation.

| File | Rows | Formula columns | Purpose |
| --- | --- | --- | --- |
| data/revised/user_dataset.csv | 100 | 2 | User norms and preferences |
| data/revised/food_ministry_dataset.csv | 100 | 2 | Public-health and regulatory norms |
| data/revised/food_industry_dataset.csv | 100 | 2 | Commercial and product-placement norms |
| data/revised/constitutive_rules.csv | 50 | 1 | Background domain classifications |

## 4.2 Parser Validation Results

The validation script was run on the revised datasets. The current result is that all formulas pass grammar validation and structural checks. No warnings or errors were reported.

data/revised/user_dataset.csv: rows=100 formulas=200 errors=0 warnings=0
data/revised/food_ministry_dataset.csv: rows=100 formulas=200 errors=0 warnings=0
data/revised/food_industry_dataset.csv: rows=100 formulas=200 errors=0 warnings=0
data/revised/constitutive_rules.csv: rows=50 formulas=50 errors=0 warnings=0
TOTAL: rows=350 formulas=650 errors=0 warnings=0
VALIDATION PASSED

These results show that the revised grammar and dataset design are syntactically consistent. However, parser success should not be interpreted as full semantic correctness. A formula can be syntactically valid while still failing to capture the intended meaning of the natural-language norm. For this reason, round-trip evaluation and human review remain necessary.

## 4.3 AST and Round-Trip Outputs

AST generation produced 350 AST records, corresponding to the 300 stakeholder norm records and 50 constitutive rules. The round-trip backtranslation pipeline produced 600 rows because each of the 300 stakeholder norms has two formal versions: implication-based and dyadic.

TOTAL AST RECORDS: 350
roundtrip rows=600
evaluated rows=600
auto score counts={'2': 538, '1': 40, '0': 22}

The automatic round-trip evaluation should be treated as a triage method rather than a final semantic metric. It is useful for identifying likely preserved cases and prioritizing possible mismatches, but human evaluation is needed to confirm whether a backtranslation preserves the original norm. This is especially important for norms containing multiple conditions, negation, disjunction, or stakeholder-specific phrasing.

Human evaluation was performed on 112 selected round-trip rows. The reviewed sample included all rows that the automatic evaluator scored as 0 or 1, plus additional quality-control examples from score-2 rows. The human reviewer judged 84 rows as semantically preserved, 22 as partially preserved, and 6 as mismatches. Exact agreement between the automatic score and the human score was 48 out of 112 reviewed rows, or 42.9%. This supports the methodological decision to treat automatic round-trip scoring as a triage signal rather than as a replacement for human semantic evaluation.

## 4.4 Claude Comparison Results

To compare LLM performance under the same dataset-generation structure, a second dataset batch was generated with Claude Opus 4.8 using high effort, the GitHub prompt files, fresh chats, and no manual edits. The Claude stakeholder datasets were generated on 2026-06-28, and the Claude constitutive rules were generated on 2026-07-03. The ChatGPT baseline model/version was recorded as ChatGPT 5.5, but the baseline effort setting was not explicitly logged, so the missing effort metadata is treated as a reproducibility limitation.

The Claude revised dataset contained 350 records and 650 formulas, matching the baseline revised dataset. Both passed the same parser validation:

| Source | Records | Formulas | Errors | Warnings |
| --- | ---: | ---: | ---: | ---: |
| Baseline revised dataset | 350 | 650 | 0 | 0 |
| Claude revised dataset | 350 | 650 | 0 | 0 |

The automatic round-trip comparison covers the 300 stakeholder records and 600 stakeholder formulas in each dataset, because constitutive rules are background classifications rather than stakeholder norms. It gave the following result:

| Source | Rows | Score 2 | Score 1 | Score 0 |
| --- | ---: | ---: | ---: | ---: |
| Baseline stakeholder datasets | 600 | 538 | 40 | 22 |
| Claude stakeholder datasets | 600 | 550 | 46 | 4 |

These results suggest that Claude followed the grammar and formalisation conventions successfully. However, the comparison report also showed that Claude used a smaller predicate vocabulary, especially for the User and Food Ministry datasets. For example, the baseline User dataset used 83 predicates, while the Claude User dataset used 48. This indicates that parser validity and round-trip score alone are not sufficient to evaluate dataset quality. Diversity, stakeholder coverage, reproducibility metadata, and usefulness for downstream DJ4ME reasoning must also be considered.

The implication-versus-dyadic comparison gave the following aggregate result:

| Source | Formula type | Valid formulas | Score 2 | Score 1 | Score 0 | Avg. AST nodes |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Baseline | Implication | 300/300 | 269 | 20 | 11 | 8.52 |
| Baseline | Dyadic | 300/300 | 269 | 20 | 11 | 7.52 |
| Claude | Implication | 300/300 | 275 | 23 | 2 | 8.56 |
| Claude | Dyadic | 300/300 | 275 | 23 | 2 | 7.56 |

The automatic round-trip score distributions were identical for implication and dyadic formulas within each source dataset. This suggests that, at the level measured by the current backtranslation heuristic, both formulations preserved the practical surface meaning of the natural-language norms equally well. However, the AST comparison showed a small structural difference: implication-based formulas produced slightly larger ASTs because they contain an explicit implication node. This should not be interpreted as a quality defect. It is a structural consequence of the representation. AST size is therefore used as a complexity indicator, not as a direct measure of correctness.

## 4.5 Discussion

### 4.5.1 Implication-Based and Dyadic Formulations

The paired dataset design directly addresses the concern that implication-based monadic norms and dyadic norms should not be mixed as if they were equivalent. By storing both formulations for the same natural-language norm, the thesis can compare their behavior while keeping the natural-language source constant. This design supports analysis of syntax validity, AST shape, and round-trip preservation across formalization strategies.

The comparison results show that both formulation types performed equally well under parser validation and automatic round-trip evaluation. All 600 implication and dyadic formulas in the baseline stakeholder dataset were parser-valid, and all 600 corresponding formulas in the Claude stakeholder dataset were also parser-valid. No paired norm received different automatic round-trip scores between its implication and dyadic versions. The main observed difference was structural: implication-based formulas had slightly larger ASTs than dyadic formulas. This is expected because implication formulas explicitly represent the conditional relation as a separate AST node, whereas dyadic formulas attach the condition directly to the modal operator.

This result supports the use of both formulations in the thesis. The value of including both is not that one is immediately shown to be better than the other, but that the dataset enables a controlled comparison without assuming semantic equivalence. For the current evaluation, both formulations appear equally robust in terms of syntax and round-trip preservation, while differing modestly in structural complexity.

### 4.5.2 Product Categories as Predicates

Treating product categories as predicates over a product variable improves the formal model. Instead of assuming that a category such as GlutenFreeMeal is a single constant, the revised formulas quantify over products and classify them through predicates. This makes the formalization compatible with a later product catalog, ontology, or knowledge base that can determine whether a particular item satisfies predicates such as glutenFreeMeal(y) or certifiedGlutenFree(y).

### 4.5.3 Constitutive Rules and Redundancy

Separating constitutive rules from stakeholder norms helps reduce redundancy and improves conceptual clarity. Stakeholder norms express what should, may, or must not be recommended. Constitutive rules define what counts as what in the food domain. This separation allows broad norms such as prohibiting non-vegan recommendations to vegan users while using background rules to classify specific products as non-vegan.

### 4.5.4 Current Limitations

The current implementation has several limitations. First, the datasets are generated and structurally validated, but the human semantic review covers a selected sample rather than all round-trip rows. Second, the round-trip evaluation is automatic and heuristic; it should support, not replace, human judgment. Third, the current work validates syntax and structure but does not yet connect formulas to a full product database or formal model interpretation. Fourth, conflict detection and dialogue-based reasoning are downstream DJ4ME tasks and are not implemented in this thesis. Finally, if LLMs are used to generate or translate additional datasets, model version, prompt, temperature, and sampling settings must be recorded because exact reproducibility cannot be guaranteed from prompts alone.

# Chapter 5: Conclusion and Future Work

## 5.1 Contributions

This thesis develops a reproducible pipeline for stakeholder norm formalization in an agent-based normative recommender-system setting. It contributes a revised dataset design that addresses semantic concerns about conditional norms, product categories, and constitutive rules. It also implements grammar-based validation, AST generation, normalized formula representations, and round-trip backtranslation outputs.

The current results demonstrate that the revised datasets can be parsed successfully under the fixed grammar. The pipeline validates 650 formulas with zero errors, generates 350 AST records, and produces 600 round-trip evaluation rows. These outputs support a focused evaluation of syntactic validity and semantic preservation in LLM-based norm formalisation.

## 5.2 Limitations

- The dataset is generated and structurally validated, but the human semantic evaluation covers a selected sample rather than every row.

- Automatic round-trip scores are heuristic and should not be treated as final truth.

- The current implementation detects syntax and structure, not full model-theoretic semantics.

- Conflict detection is not part of the implemented thesis scope; it is treated as downstream DJ4ME future work.

- The domain predicates assume a future product catalog or knowledge base for interpretation.

- Using LLMs for data generation introduces reproducibility limits unless model settings and outputs are archived. In the current work, the Claude Opus 4.8 high-effort generation metadata was recorded, and the ChatGPT baseline model/version was recorded as ChatGPT 5.5, but the baseline effort setting was not explicitly logged.

## 5.3 Future Work

Future work can connect the parser-validated norms to the wider DJ4ME reasoning architecture. One direction is conflict detection over normalized AST representations, beginning with direct modality conflicts such as obligations and prohibitions concerning the same recommendation action under overlapping conditions. This is outside the implemented scope of the thesis but is a natural downstream use of the generated ASTs and constitutive rules.

A second next step is human evaluation of round-trip semantic preservation. A reviewer can inspect the original natural-language norms, formulas, and backtranslations, then assign human semantic scores and error categories. These human scores can be compared with the automatic scores to determine where the automatic method is reliable and where it fails.

A third direction is to integrate the formalized norms into stakeholder-avatar dialogue. In the DJ4ME setting, such norms could become inputs for avatars that make claims, provide reasons, concede or retract claims, and participate in persuasion dialogue.

Finally, the thesis can be extended by testing additional LLMs or prompt strategies for the NL-to-logic translation task. The evaluation can measure syntax validity, semantic preservation, parser error rates, correction effort, vocabulary diversity, and usefulness for downstream DJ4ME components.

# Bibliography

[0] DJ4ME Project Proposal. A DJ for Machine Ethics: the Dialogue Jiminy. FullProposal18989918.pdf, pages 9-20 used for project context.

[1] Harnessing the Power of Large Language Models for Natural Language to First-Order Logic Translation. arXiv:2305.15541.

[2] FOLIO: Natural Language Reasoning with First-Order Logic. arXiv:2209.00840.

[3] Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning. arXiv:2305.12295.

[4] Multi-Stakeholder Recommendation: Applications and Challenges. arXiv:1707.08913.

[5] Multi-stakeholder Recommendation and its Connection to Multi-sided Fairness. arXiv:1907.13158.

[6] A Defeasible Deontic Calculus for Resolving Norm Conflicts. arXiv:2407.04869.

[7] Dung, P. M. On the Acceptability of Arguments and its Fundamental Role in Nonmonotonic Reasoning, Logic Programming and n-Person Games.

[8] Personalized Food Recommendation as Constrained Question Answering over a Large-Scale Food Knowledge Graph. arXiv:2101.01775.

Draft note: Before submission, convert this bibliography into the citation style required by the programme and cite sources inline throughout Chapters 1 and 2.

# Appendix A: Repository and Reproducibility

The current repository is llm-normative-recommender. Older folders have been archived under archive/previous_structure. The active pipeline folders are data, prompts, grammar, scripts, outputs, and docs.

python scripts/generate_revised_user_dataset.py
python scripts/generate_revised_food_ministry_dataset.py
python scripts/generate_revised_food_industry_dataset.py
python scripts/generate_constitutive_rules.py
python scripts/validate_revised_datasets.py
python scripts/generate_asts.py
python scripts/backtranslate_roundtrip.py
python scripts/evaluate_roundtrip.py

# Appendix B: Example Dataset Record

| Field | Value |
| --- | --- |
| id | USER001 |
| stakeholder | User |
| nl_norm | Children should not receive energy drink recommendations. |
| implication_formula | ∀x.∀y.child(x)∧energyDrink(y)->F(recommend(System,y,x)) |
| dyadic_formula | ∀x.∀y.F(recommend(System,y,x)\|child(x)∧energyDrink(y)) |
| norm_type | prohibition |

# Appendix C: Human Evaluation Form

The round-trip evaluation file contains columns for human review. Reviewers should compare the original natural-language norm with the backtranslated natural-language statement and assign a score.

| Human score | Interpretation |
| --- | --- |
| 2 | The backtranslation preserves the original norm. |
| 1 | The backtranslation partially preserves the norm but loses or weakens some information. |
| 0 | The backtranslation does not preserve the intended norm. |
