# ChatGPT V2 Final Human Review Summary

This file transfers the existing ChatGPT human-review labels onto the v2 backtranslation output and adds fresh human review for the two `USER030` rows whose v2 backtranslation exposed an operator-precedence issue. Most v2 changes are stylistic rewrites of compound conditions, for example changing `A and B` into `all of the following hold: A; and B`.

## Files

- Final CSV: `outputs/roundtrip_v2/roundtrip_evaluated_v2_final_human.csv`
- Final JSON: `outputs/roundtrip_v2/roundtrip_evaluated_v2_final_human.json`
- Review candidate file: `outputs/roundtrip_v2/chatgpt_v2_changed_backtranslation_human_review_candidates.csv`
- Source v1 human file: `outputs/roundtrip/baseline_roundtrip_human_evaluated.csv`
- Source v2 evaluated file: `outputs/roundtrip_v2/roundtrip_evaluated_v2.csv`

## Review Counts

- Total rows in final dataset: 600
- Human-reviewed rows in final dataset: 112
- Previous human-reviewed rows copied into v2: 110
- Fresh v2 human-reviewed rows added: 2
- Rows not part of the reviewed sample: 488

## Human Scores

- Human score 0: 4
- Human score 1: 24
- Human score 2: 84

## Human Error Types

- awkward_but_equivalent: 36
- lost_meaning: 10
- missing_condition: 2
- none: 48
- wrong_action: 6
- wrong_condition: 10

## Automatic Score vs Human Score

- Auto 0 -> Human 1: 4
- Auto 0 -> Human 2: 18
- Auto 1 -> Human 0: 4
- Auto 1 -> Human 1: 8
- Auto 1 -> Human 2: 26
- Auto 2 -> Human 1: 12
- Auto 2 -> Human 2: 40

## USER030 Review Decision

Both `USER030` rows have automatic score 2 because the v2 backtranslation faithfully reflects the formula. However, human review marks them as score 1 with `wrong_condition` because the formula's condition is parsed as `allergicTo(x,Nuts) ∨ (allergicTo(x,Shellfish) ∧ allergenSafeMeal(y))`, while the original natural-language norm appears to intend `(allergicTo(x,Nuts) ∨ allergicTo(x,Shellfish)) ∧ allergenSafeMeal(y)`.
