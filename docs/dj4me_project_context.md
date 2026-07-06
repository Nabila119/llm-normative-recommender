# DJ4ME Project Context Notes

Source: `FullProposal18989918.pdf`, pages 9-20.

These notes summarize the parts of the DJ4ME proposal that are relevant to the thesis.

## Project Aim

DJ4ME stands for **A DJ for Machine Ethics: the Dialogue Jiminy**. The project studies how autonomous agents can make ethical decisions when their actions affect multiple stakeholders. It builds on the earlier Autonomous Jiminy idea, where stakeholder norms are combined into arguments to identify and resolve moral dilemmas.

The DJ4ME proposal moves from an autonomous moral advisor toward a **Dialogue Jiminy**, where stakeholder avatars can participate in persuasion dialogue. The motivation is that stakeholders should not merely have their norms aggregated by the system; their avatars should be able to choose recommendation strategies and participate in dialogue.

## Core Research Questions in DJ4ME

The proposal frames DJ4ME around three questions:

1. How can autonomous agents behave ethically in possible scenarios using stakeholders' views on ethical argumentation as inputs?
2. How can the agent understand stakeholders' norms and explain its final decision afterwards?
3. How can the system be demonstrated and promoted for machine ethics among the general population?

This thesis is most closely connected to the second question, especially the part concerning how an agent can understand stakeholder norms.

## Relevant Objective

The most directly relevant project objective is **Objective 2: Norm mining and explanation synthesis**.

This objective includes creating a natural-language interface between Dialogue Jiminy and stakeholders. The interface has two language tasks:

- transforming informal stakeholder norms into formal avatar rules;
- generating natural-language explanations of formal recommendations or dialogues.

This thesis focuses on the first of these tasks: converting stakeholder norms from natural language into a controlled deontic first-order logic representation and evaluating whether that conversion is syntactically valid and semantically preserved.

## Theoretical Background Used by DJ4ME

The proposal connects several areas:

- machine ethics;
- deontic logic;
- normative systems;
- formal argumentation;
- argumentation as dialogue;
- machine learning and LLM-based language interfaces.

For this thesis, the most relevant concepts are deontic logic, normative systems, constitutive norms, and LLM-based norm formalisation.

## Deontic Logic and Normative Systems

The proposal describes deontic logic as the study of obligations and permissions in ethical or legal domains. It also notes that standard deontic logic has been extended with dyadic representations of conditional obligations and with non-monotonic features to handle conflicts and deontic paradoxes.

The proposal also discusses normative systems, where modalities can be represented more implicitly through conditional norms. It explicitly mentions constitutive norms, where one fact counts as or gives rise to another institutional fact. This supports the thesis design choice to keep constitutive rules separate from stakeholder obligations, permissions, and prohibitions.

## Language Interface and LLMs

The proposal identifies two machine-learning tasks for the Jiminy language interface:

- norm mining;
- explanation synthesis.

It mentions both generative LLMs and non-generative LLMs. Generative LLMs are expected to help retrieve relevant normative information and provide symbolic expressions for norms. Non-generative models are discussed for classification tasks such as recognizing obligations, permissions, and constitutive rules.

This thesis contributes to the norm-formalisation side of this language interface by studying whether LLM-generated stakeholder norms can be represented in a fixed formal grammar, parsed, transformed into ASTs, and evaluated through round-trip semantic preservation.

## Case Study Relevance

The DJ4ME proposal includes food and nutrition recommender systems as one of its case studies. It links this case study to explainable nutrition virtual coaches and food recommender systems, noting transparency as an important issue. It identifies relevant stakeholders such as users, nutritionists, parents, and food industry actors.

This thesis uses a food recommender setting with three stakeholder perspectives:

- User;
- Food Ministry;
- Food Industry.

This fits the DJ4ME case-study direction while narrowing the implementation scope to dataset construction, formalisation, parser validation, LLM comparison, and semantic evaluation.

## How This Thesis Fits DJ4ME

This thesis does not implement the full Dialogue Jiminy system. It provides an upstream dataset and evaluation pipeline for one part of the DJ4ME language interface:

```text
stakeholder natural-language norm
-> deontic first-order logic formula
-> parser validation
-> AST generation
-> round-trip semantic evaluation
-> future use in dialogue, explanation, or conflict analysis
```

The thesis therefore supports DJ4ME by producing reusable, parser-validated formal norms that could later be used by avatars in argumentation or dialogue systems.
