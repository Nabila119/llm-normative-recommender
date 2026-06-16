# Thesis

Title: Leveraging LLMs for Agent-Based Normative Recommender Systems

Goal:
- Extract stakeholder norms using LLMs
- Formalize norms into deontic first-order logic
- Validate formulas using a parser
- Generate ASTs
- Detect conflicts between norms

Stakeholders:
- Users
- Food Ministry
- Food Industry

# Formal Representation

We use deontic first-order modal logic.

Modal operators:
- O = Obligation
- P = Permission
- F = Prohibition

Supports:
- Quantifiers (∀, ∃)
- Predicates
- Functions
- Dyadic norms O(p | q)
- Implication q → O(p)

# Grammar

[paste current grammar.lark here]

# Current Goal

Implement a parser using Python and Lark.

Requirements:
- Parse formulas
- Generate ASTs
- Reject invalid formulas
- Ensure deterministic parsing

# Current Error

Formula:
∀x. F(recommend(System,EnergyDrink) | child(x))

Error:
Unexpected token ',' at column 23.

Need help debugging lexer/token ambiguity.