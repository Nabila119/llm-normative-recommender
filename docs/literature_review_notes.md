# Literature Review Notes

This file summarizes recommended papers for the thesis and explains how each paper relates to the current work on LLM-based norm formalization for agent-based normative recommender systems.

The thesis focus is:

```text
Natural language stakeholder norms
-> modal/deontic first-order logic
-> grammar/parser validation
-> AST generation
-> round-trip semantic preservation
-> conflict detection
```

## 1. Harnessing the Power of Large Language Models for Natural Language to First-Order Logic Translation

Link: https://arxiv.org/pdf/2305.15541

### Why Read It

This is one of the most directly relevant papers because it studies natural language to first-order logic translation using LLMs. It also discusses dataset generation, prompt design, grammar validation, correction, and evaluation.

### Similarity To This Thesis

Both works study the translation of natural language into formal logic. Both use LLMs as part of the translation pipeline. Both require grammar-constrained outputs and validation of generated formulas.

### What They Did

The authors introduced LOGICLLAMA, a LLaMA-based model fine-tuned for NL-to-FOL translation. They created MALLS, a large GPT-4-generated dataset of natural language and FOL pairs. Their pipeline used dynamic prompting, few-shot examples, n-gram diversity control, grammar-based verification, and correction strategies.

### What We Can Learn

- Use a fixed grammar during generation and validation.
- Treat LLM-generated datasets as silver-label data unless manually verified.
- Use parser validation as a core metric.
- Use prompt strategies to improve diversity and formula quality.
- Avoid overly compressed predicates that hide logical structure.
- Consider correction or refinement after invalid formula generation.

### Limitations

- The generated dataset is silver-label, not fully expert-verified.
- Semantic alignment between natural language and FOL is only weakly checked.
- The paper focuses on standard FOL, not modal or deontic FOL.
- It does not address stakeholder norms or conflict detection.

### Can This Thesis Address The Limitations?

Partly. This thesis can address semantic alignment more directly through round-trip evaluation:

```text
natural language -> modal FOL -> natural language
```

It also extends the setting from standard FOL to modal/deontic FOL and applies it to stakeholder norms. However, this thesis will likely remain smaller in dataset size and will not fine-tune a model like LOGICLLAMA.

## 2. FOLIO: Natural Language Reasoning with First-Order Logic

Link: https://arxiv.org/abs/2209.00840

### Why Read It

FOLIO is important because it provides a human-annotated dataset for natural language reasoning with first-order logic annotations. It is commonly used in NL-to-FOL and logical reasoning research.

### Similarity To This Thesis

Both works use paired natural language and formal logic representations. Both treat formal logic as a way to support reasoning beyond surface-level natural language processing.

### What They Did

The authors created a dataset of natural language premises and conclusions paired with FOL annotations. The annotations support reasoning tasks and can be checked using formal inference tools.

### What We Can Learn

- Expert or manually checked logic annotations are valuable for evaluation.
- Formal annotations can support downstream reasoning.
- NL-to-logic datasets should be evaluated not only by syntax but also by reasoning usefulness.
- A smaller carefully validated dataset can be more useful than a large noisy dataset.

### Limitations

- FOLIO focuses on general first-order logic reasoning, not deontic or modal norms.
- It is not specific to recommender systems.
- It does not focus on stakeholder conflicts.

### Can This Thesis Address The Limitations?

Yes, by applying NL-to-logic translation to a new domain: stakeholder norms in food recommender systems. The thesis can also add modal operators such as obligation, permission, and prohibition, which are outside FOLIO's main focus.

## 3. Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning

Link: https://arxiv.org/abs/2305.12295

### Why Read It

This paper is important because it uses LLMs to translate natural language into symbolic representations and then delegates reasoning to symbolic solvers. This is close to the planned pipeline of translating norms into modal FOL and then using parser/AST-based tools for validation and conflict detection.

### Similarity To This Thesis

Both approaches use LLMs for translation and symbolic tools for more reliable reasoning. The shared idea is that LLMs are useful for language understanding, while formal tools are better for validation and structured reasoning.

### What They Did

The authors proposed a framework where LLMs translate natural language reasoning problems into formal symbolic representations. Symbolic solvers are then used to perform faithful reasoning. They also use solver feedback to refine incorrect symbolic formulations.

### What We Can Learn

- Hybrid LLM-symbolic pipelines can be more reliable than LLM-only reasoning.
- Formal representations act as an intermediate layer between language and reasoning.
- Parser or solver feedback can be used to improve generated formulas.
- The thesis can justify using ASTs and conflict-detection tools rather than relying only on LLM judgment.

### Limitations

- The paper focuses on logical reasoning benchmarks rather than normative recommender systems.
- It does not focus on deontic concepts such as obligations and prohibitions.
- It depends on symbolic solvers, while this thesis may use a custom parser and conflict detector.

### Can This Thesis Address The Limitations?

Partly. This thesis adapts the general LLM-symbolic idea to a domain-specific normative setting. Instead of using a general solver, it can use a controlled grammar, ASTs, and conflict-detection rules tailored to stakeholder norms.

## 4. Multi-Stakeholder Recommendation: Applications and Challenges

Link: https://arxiv.org/abs/1707.08913

### Why Read It

This paper is useful for justifying why the thesis considers multiple stakeholders rather than only users. It provides background for recommender systems where several parties have interests in the recommendation outcome.

### Similarity To This Thesis

Both works recognize that recommender systems involve more than one stakeholder. This thesis uses User, Food Ministry, and Food Industry as stakeholder perspectives.

### What They Did

The paper discusses applications and challenges in multi-stakeholder recommendation, where recommendation outcomes must account for the interests of several parties.

### What We Can Learn

- Multi-stakeholder recommender systems naturally involve competing objectives.
- Stakeholder interests may conflict.
- Evaluation should consider more than user satisfaction.
- This supports the need for conflict detection between stakeholder norms.

### Limitations

- The paper is not about formal logic.
- It does not provide a deontic representation of stakeholder requirements.
- It does not use LLMs for norm translation.

### Can This Thesis Address The Limitations?

Yes. This thesis can use the multi-stakeholder recommender framing and add a formal norm representation layer. It contributes a way to translate stakeholder requirements into modal FOL for validation and conflict analysis.

## 5. Multi-Stakeholder Recommendation and Its Connection to Multi-Sided Fairness

Link: https://arxiv.org/abs/1907.13158

### Why Read It

This paper helps situate stakeholder conflicts within broader fairness and accountability concerns in recommender systems.

### Similarity To This Thesis

Both works are concerned with the effects of recommendations on multiple parties. This thesis can use it to motivate why stakeholder norms must be represented and analyzed explicitly.

### What They Did

The authors connect multi-stakeholder recommendation with multi-sided fairness, showing that recommender systems may need to balance fairness concerns across different groups.

### What We Can Learn

- Stakeholder conflict is not only technical but also ethical and societal.
- Fairness can be multi-sided, involving users, providers, platforms, and other affected parties.
- This supports the thesis significance section.

### Limitations

- The paper focuses on fairness and recommender-system design, not formal norm translation.
- It does not provide modal-FOL representations or parser validation.
- It does not discuss LLM-generated formalizations.

### Can This Thesis Address The Limitations?

Yes, at least partially. The thesis can provide a formal representation and analysis pipeline for stakeholder norms, complementing fairness-oriented recommender research.

## 6. A Defeasible Deontic Calculus for Resolving Norm Conflicts

Link: https://arxiv.org/abs/2407.04869

### Why Read It

This paper is useful for the conflict-detection and conflict-resolution part of the thesis. It shows that norm conflicts are theoretically complex and may require defeasible reasoning or priorities.

### Similarity To This Thesis

Both works are concerned with norms, obligations, and conflicts. This thesis may detect conflicts between stakeholder norms, while this paper studies more formal mechanisms for resolving conflicts.

### What They Did

The authors propose a defeasible deontic calculus for resolving norm conflicts. The work connects deontic logic with normative multi-agent systems and studies how conflicts between norms can be handled.

### What We Can Learn

- Conflict detection is different from conflict resolution.
- Resolving conflicts often requires priorities, exceptions, or defeasibility.
- This supports a limitation in the thesis: detecting direct conflicts is feasible, but full conflict resolution may be future work.

### Limitations

- The paper is more theoretical and may be difficult to implement fully within the thesis timeline.
- It is not about LLM-based norm translation.
- It does not focus on recommender systems.

### Can This Thesis Address The Limitations?

Partly. This thesis can focus on conflict detection rather than full conflict resolution. It can mention that resolving conflicts using priorities or defeasible reasoning is an important future extension.

## 7. Dung's Abstract Argumentation Framework

Reference: Phan Minh Dung, "On the Acceptability of Arguments and its Fundamental Role in Nonmonotonic Reasoning, Logic Programming and n-Person Games"

Overview link: https://en.wikipedia.org/wiki/Argumentation_framework

### Why Read It

This is relevant because the supervisor mentioned Dung semantics. Abstract argumentation provides a formal way to model conflicts as attacks between arguments and then determine which arguments are acceptable.

### Similarity To This Thesis

Both concern conflicting information. In this thesis, conflicting stakeholder norms could be represented as attacks between arguments or norm-derived claims.

### What They Did

Dung introduced abstract argumentation frameworks, where arguments are nodes and attacks are directed edges. Different semantics, such as grounded, preferred, and stable semantics, determine which sets of arguments can be accepted.

### What We Can Learn

- Conflicts can be represented as attack relations.
- Conflict resolution may require a semantics, not just pairwise detection.
- If stakeholder priorities are added later, argumentation can provide a formal framework.

### Limitations

- The framework is abstract and does not itself specify how natural language norms become arguments.
- It does not provide NL-to-logic translation.
- It requires a method for constructing arguments and attack relations.

### Can This Thesis Address The Limitations?

Partly. This thesis can use AST-based conflict detection to construct potential attack relations, while leaving full Dung-style evaluation as future work unless time allows.

## 8. Personalized Food Recommendation as Constrained Question Answering over a Large-Scale Food Knowledge Graph

Link: https://arxiv.org/abs/2101.01775

### Why Read It

This paper supports the food recommendation domain. It shows how food recommendation can be treated as a constrained reasoning problem over structured knowledge.

### Similarity To This Thesis

Both works concern food recommendation and constraints. This thesis focuses on normative constraints, while the paper focuses on food recommendation using knowledge graphs.

### What They Did

The authors formulate personalized food recommendation as constrained question answering over a large-scale food knowledge graph.

### What We Can Learn

- Food recommendation often requires structured knowledge about foods, ingredients, nutrition, and user needs.
- Product properties can be represented as structured facts rather than vague labels.
- This supports the professor's point about representing product categories as predicates over product variables.

### Limitations

- The paper is not about deontic logic or normative systems.
- It does not translate stakeholder norms into modal FOL.
- It focuses on recommendation rather than norm formalization.

### Can This Thesis Address The Limitations?

Yes, by focusing specifically on norms and formal logic rather than recommendation ranking. The thesis can also mention that a full food knowledge graph is outside scope, but a small toy interpretation or product-fact layer could ground predicates such as `glutenFreeMeal(y)` or `contains(y,Nuts)`.

## 9. Classification of Normative Recommender Systems

Link: https://www.researchgate.net/publication/375666532_Classification_of_Normative_Recommender_Systems

### Why Read It

This is highly relevant because it directly concerns normative recommender systems. It can help position the thesis within recommender systems that incorporate norms and values.

### Similarity To This Thesis

Both works are concerned with recommendations that are shaped by norms rather than only user preferences. This thesis contributes a formal norm-translation and validation pipeline.

### What They Did

The paper classifies ways in which norms can be integrated into recommender systems, such as before, during, or after recommendation generation, and through evaluation.

### What We Can Learn

- Norms can influence recommender systems at multiple stages.
- The thesis can position formal norm translation as a preprocessing or knowledge-representation step.
- The work supports the argument that norm-aware recommendation is an emerging research direction.

### Limitations

- The paper is classification-oriented and does not provide a full NL-to-modal-FOL translation pipeline.
- It does not focus on parser validation, ASTs, or LLM-generated formulas.
- It may not address formal conflict detection in the way this thesis aims to.

### Can This Thesis Address The Limitations?

Yes. This thesis can provide a concrete technical pipeline that complements the conceptual classification of normative recommender systems.

## 10. Health-Aware Food Recommendation Based on Knowledge Graph and Multi-Task Learning

Link: https://pmc.ncbi.nlm.nih.gov/articles/PMC10216993/

### Why Read It

This paper provides background for health-aware food recommendation. It is useful for motivating norms about diabetes, hypertension, low sugar, low salt, allergies, and healthy alternatives.

### Similarity To This Thesis

Both are concerned with food recommendation under health-related constraints. This thesis represents those constraints as stakeholder norms rather than directly optimizing recommendations.

### What They Did

The authors propose a health-aware food recommendation approach using knowledge graphs and multi-task learning.

### What We Can Learn

- Health constraints are central in food recommendation.
- Structured food knowledge helps connect user conditions to suitable foods.
- The thesis can use this to justify health-related normative categories.

### Limitations

- The paper is not about formal norm translation.
- It does not use deontic logic.
- It does not compare LLM-based NL conflict detection with logic-based conflict detection.

### Can This Thesis Address The Limitations?

Partly. The thesis does not build a full health-aware recommender, but it can formalize health-related norms that such systems should obey.

## 11. PREFer: A Prescription-Based Food Recommender System

Link: https://www.sciencedirect.com/science/article/pii/S0920548916301301

### Why Read It

This paper is useful for understanding food recommendation under prescriptions, health conditions, and user constraints.

### Similarity To This Thesis

Both works involve food recommendations constrained by health or prescription-like rules. This thesis focuses on translating such constraints into formal norms.

### What They Did

The paper presents a prescription-based food recommender system that considers user health needs and food suitability.

### What We Can Learn

- Food recommendation often involves more than preference matching.
- Some recommendation rules are normative in spirit, such as avoiding foods unsuitable for medical conditions.
- The thesis can use this to motivate why obligations and prohibitions matter in food recommendation.

### Limitations

- It does not focus on LLMs.
- It does not formalize norms in modal FOL.
- It does not compare natural-language and logic-based conflict detection.

### Can This Thesis Address The Limitations?

Yes, by proposing a formal norm representation and evaluation pipeline around food recommendation constraints.

## Recommended Reading Order

If time is limited, read in this order:

1. Harnessing the Power of Large Language Models for Natural Language to First-Order Logic Translation
2. FOLIO: Natural Language Reasoning with First-Order Logic
3. Logic-LM
4. Multi-Stakeholder Recommendation: Applications and Challenges
5. Classification of Normative Recommender Systems
6. A Defeasible Deontic Calculus for Resolving Norm Conflicts
7. Dung's Abstract Argumentation Framework
8. Food recommendation papers

## How These Papers Support The Thesis

Together, these works support the thesis as follows:

- NL-to-FOL papers justify the translation task and grammar validation.
- Logic-LM-style work justifies combining LLMs with symbolic tools.
- Multi-stakeholder recommendation papers justify the stakeholder setup.
- Normative recommender papers justify the normative recommender framing.
- Deontic and argumentation papers justify conflict detection and future conflict resolution.
- Food recommendation papers justify the domain and the need for health, dietary, and product constraints.

## Possible Thesis Gap Statement

Existing work studies LLM-based natural-language-to-logic translation, multi-stakeholder recommendation, normative reasoning, and food recommendation under constraints. However, limited work combines these directions into a reproducible pipeline for translating stakeholder food recommendation norms into parser-validated modal first-order logic, generating AST representations, evaluating semantic preservation through round-trip translation, and comparing natural-language-based conflict detection with logic-based conflict detection.

