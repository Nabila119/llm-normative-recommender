# Implication vs Dyadic Formulation Comparison

This report compares the paired implication-based and dyadic formulas generated for the same natural-language stakeholder norms.

Implication formulas place the condition outside the deontic operator: `condition -> O(action)`.

Dyadic formulas place the condition inside the deontic operator: `O(action | condition)`.

## Aggregate Results

| Source | Formula type | Formulas | Parser valid | Expected pattern | Score 2 | Score 1 | Score 0 | Avg AST nodes | Avg AST depth | Avg predicates |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | dyadic | 300 | 300 | 300 | 269 | 20 | 11 | 7.52 | 5.29 | 3.23 |
| baseline | implication | 300 | 300 | 300 | 269 | 20 | 11 | 8.52 | 5.31 | 3.23 |
| claude | dyadic | 300 | 300 | 300 | 275 | 23 | 2 | 7.56 | 5.34 | 3.22 |
| claude | implication | 300 | 300 | 300 | 275 | 23 | 2 | 8.56 | 5.37 | 3.22 |

## Paired Round-Trip Score Differences

Rows where implication and dyadic formulas for the same norm received different automatic round-trip scores: 0.

## Interpretation

This comparison does not treat the two formula types as semantically identical. Instead, it evaluates how the two rival formalisation strategies behave when applied to the same natural-language norms.

The key thesis use is to compare syntax compliance, round-trip semantic preservation, and AST-level structural complexity under controlled input conditions.