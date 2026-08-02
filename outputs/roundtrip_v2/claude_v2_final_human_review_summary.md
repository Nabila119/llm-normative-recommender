# Claude V2 Final Human Review Summary

This file combines the new Claude v2 low-score human review with a score-2 sample inherited from the earlier Claude human review file. Older score-2 labels were copied only when the id, stakeholder, formula type, norm type, original natural-language norm, formula, and automatic score-2 status matched in v2.

## Files

- Final CSV: `outputs/roundtrip_v2/claude_roundtrip_evaluated_v2_final_human.csv`
- Final JSON: `outputs/roundtrip_v2/claude_roundtrip_evaluated_v2_final_human.json`
- Source v2 merged file: `outputs/roundtrip_v2/claude_roundtrip_evaluated_v2_human_merged.csv`
- Source v1 human file: `outputs/roundtrip/claude_roundtrip_human_evaluated.csv`

## Review Counts

- Total rows in final dataset: 600
- Human-reviewed rows in final dataset: 68
- New v2 low-score reviewed rows preserved: 18
- Inherited score-2 sample rows from v1: 50
- Inherited rows with exact same backtranslation text: 2
- Inherited rows with v2 reworded but same original norm and formula: 48

## Human Scores

- Human score 1: 5
- Human score 2: 63

## Human Error Types

- missing_condition: 3
- none: 63
- wrong_condition: 2

## Automatic Score vs Human Score

- Auto 0 -> Human 2: 4
- Auto 1 -> Human 1: 2
- Auto 1 -> Human 2: 12
- Auto 2 -> Human 1: 3
- Auto 2 -> Human 2: 47

## Notes

- The inherited score-2 sample is used to ensure the final v2 file contains human-reviewed examples from the high automatic-score group, not only the low-score group.
- V2 backtranslation often changes wording for compound conditions, so exact backtranslation text is not required for inheritance; the inherited rows keep the same original norm and formal formula and remain automatic score 2 in v2.
- Rows without a human score remain blank and were not part of the human-reviewed sample.
