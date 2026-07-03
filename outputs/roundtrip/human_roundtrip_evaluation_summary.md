# Human Round-Trip Evaluation Summary

Reviewer: Viktor

Input file: `outputs/roundtrip/baseline_roundtrip_human_evaluated.csv`

## Coverage

| Measure | Count |
|---|---:|
| Total round-trip rows | 600 |
| Human-reviewed rows | 112 |
| Not human-reviewed rows | 488 |

## Human Semantic Scores

| Score | Meaning | Count |
|---|---|---:|
| 2 | Semantically preserved | 84 |
| 1 | Partially preserved | 22 |
| 0 | Semantic mismatch | 6 |

## Human Error Types

| Error type | Count |
|---|---:|
| none | 48 |
| awkward_but_equivalent | 36 |
| lost_meaning | 12 |
| wrong_condition | 8 |
| wrong_action | 6 |
| missing_condition | 2 |

## Reviewed Rows by Stakeholder

| Stakeholder | Score 2 | Score 1 | Score 0 | Total reviewed |
|---|---:|---:|---:|---:|
| User | 32 | 2 | 2 | 36 |
| Food Ministry | 20 | 14 | 4 | 38 |
| Food Industry | 32 | 6 | 0 | 38 |

## Reviewed Rows by Formula Type

| Formula type | Score 2 | Score 1 | Score 0 | Total reviewed |
|---|---:|---:|---:|---:|
| implication | 42 | 11 | 3 | 56 |
| dyadic | 42 | 11 | 3 | 56 |

## Automatic vs Human Scores on Reviewed Rows

| Measure | Value |
|---|---:|
| Exact auto-human agreement | 48/112 |
| Exact auto-human agreement percent | 42.9% |
| Auto score 2 in reviewed set | 50 |
| Auto score 1 in reviewed set | 40 |
| Auto score 0 in reviewed set | 22 |

Interpretation: the automatic score is useful as a triage signal but does not replace human semantic review. Many disagreements show that the heuristic can be conservative for faithful formulas or over-optimistic for generic stakeholder wording that was narrowed in the formula.

## Thesis Wording

A human reviewer evaluated 112 selected round-trip rows. Of these, 84 were judged semantically preserved, 22 partially preserved, and 6 mismatched. The reviewed sample included all rows that the automatic evaluator scored as 0 or 1, plus quality-control samples from score-2 rows. Exact agreement between the automatic and human scores was 42.9%, which confirms that automatic round-trip evaluation should be treated as a triage mechanism rather than a final semantic metric.
