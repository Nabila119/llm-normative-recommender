# ChatGPT V2 Final Human Review Summary

This file transfers the existing ChatGPT human-review labels onto the v2 backtranslation output. Most v2 changes are stylistic rewrites of compound conditions, for example changing `A and B` into `all of the following hold: A; and B`. The only rows left for fresh human review are the two `USER030` rows, where the v1 backtranslation was malformed and v2 changed the review target.

## Files

- Final CSV: `outputs/roundtrip_v2/roundtrip_evaluated_v2_final_human.csv`
- Final JSON: `outputs/roundtrip_v2/roundtrip_evaluated_v2_final_human.json`
- Rows needing fresh review: `outputs/roundtrip_v2/chatgpt_v2_changed_backtranslation_human_review_candidates.csv`
- Source v1 human file: `outputs/roundtrip/baseline_roundtrip_human_evaluated.csv`
- Source v2 evaluated file: `outputs/roundtrip_v2/roundtrip_evaluated_v2.csv`

## Review Counts

- Total rows in final dataset: 600
- Previous human-reviewed rows copied into v2: 110
- Rows left for fresh human review: 2
- Rows not part of the reviewed sample: 490

## Human Scores Currently Present

- Human score 0: 4
- Human score 1: 22
- Human score 2: 84

## Human Error Types Currently Present

- awkward_but_equivalent: 36
- lost_meaning: 10
- missing_condition: 2
- none: 48
- wrong_action: 6
- wrong_condition: 8

## Automatic Score vs Human Score Currently Present

- Auto 0 -> Human 1: 4
- Auto 0 -> Human 2: 18
- Auto 1 -> Human 0: 4
- Auto 1 -> Human 1: 8
- Auto 1 -> Human 2: 26
- Auto 2 -> Human 1: 10
- Auto 2 -> Human 2: 40

## Rows Requiring Fresh Review

- USER030 (implication): auto score 2, `none`
- USER030 (dyadic): auto score 2, `none`

After these two rows are reviewed, their `human_semantic_score`, `human_error_type`, and `human_notes` values can be merged back into the final CSV.
