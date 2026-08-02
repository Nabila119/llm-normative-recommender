# Claude V2 Human Review Summary

Reviewed rows merged into full Claude V2 dataset: 18

The reviewed rows are all Claude V2 records whose automatic score was 0 or 1.

## Human Score Counts

- Score 1: 2
- Score 2: 16

## Human Error Type Counts

- none: 16
- wrong_condition: 2

## Auto-Human Crosstab

- Auto 0 -> Human 2: 4
- Auto 1 -> Human 1: 2
- Auto 1 -> Human 2: 12

## Interpretation

Most low automatic scores were judged faithful by human review, indicating that the automatic evaluator remained conservative even after the V2 backtranslation improvement. The two human score-1 rows are wrong-condition cases where the formula/backtranslation changed the product condition from certified meals to healthy meals.

## Files

- Full merged CSV: `outputs/roundtrip_v2/claude_roundtrip_evaluated_v2_human_merged.csv`
- Full merged JSON: `outputs/roundtrip_v2/claude_roundtrip_evaluated_v2_human_merged.json`
- Reviewed candidate CSV: `outputs/roundtrip_v2/claude_v2_score_0_1_human_review_candidates.csv`
