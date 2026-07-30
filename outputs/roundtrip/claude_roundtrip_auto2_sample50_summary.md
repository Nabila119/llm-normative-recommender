# Claude Auto-2 Sample 50 Summary

Source file: `outputs/roundtrip/claude_roundtrip_evaluated.csv`

Output file: `outputs/roundtrip/claude_roundtrip_auto2_sample50_human_review_candidates.csv`

Sampling seed: `42`

Sampling design: 50 rows from Claude rows with `auto_semantic_score = 2`, balanced as 25 implication and 25 dyadic. Within each formula type, the sample uses 8 User rows, 9 Food Ministry rows, and 8 Food Industry rows. The human columns have now been scored.

## Counts

- Total sampled rows: 50
- Auto score distribution: {'2': 50}
- Human score distribution: {'1': 3, '2': 47}
- Human error type distribution: {'missing_condition': 3, 'none': 47}
- Formula type distribution: {'dyadic': 25, 'implication': 25}
- Stakeholder distribution: {'Food Industry': 16, 'Food Ministry': 18, 'User': 16}

## By Formula Type

- dyadic: score 2 = 22, score 1 = 3, score 0 = 0
- implication: score 2 = 25, score 1 = 0, score 0 = 0

## By Stakeholder

- Food Industry: score 2 = 14, score 1 = 2, score 0 = 0
- Food Ministry: score 2 = 18, score 1 = 0, score 0 = 0
- User: score 2 = 15, score 1 = 1, score 0 = 0

## Rows Marked 1

- INDUSTRY048 (dyadic, Food Industry): Partially preserved: the permission and seasonal product condition are preserved, but the new product alternative from the original/formula is missing in the backtranslation.
- INDUSTRY050 (dyadic, Food Industry): Partially preserved: the permission and affordable product condition are preserved, but the discounted product alternative from the original/formula is missing in the backtranslation.
- USER062 (dyadic, User): Partially preserved: the permission and vegan user + vegetarian meal condition are preserved, but the vegetarian user alternative from the original/formula is missing in the backtranslation.
