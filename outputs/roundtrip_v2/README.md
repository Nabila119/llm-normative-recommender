# Round-Trip Backtranslation V2

This folder preserves an experimental second version of the round-trip backtranslation outputs. The original files in `outputs/roundtrip/` were not changed.

## Why V2 Was Added

The original backtranslation script sometimes simplified compound conditions, especially disjunctions such as `diabetic(x)∨hypertensive(x)` or product alternatives such as `energyDrink(y)∨sugarySnack(y)`. This could make the backtranslation omit one condition and create a partial-preservation error even when the generated formula itself contained the missing condition.

## What Changed

The script `scripts/backtranslate_roundtrip_v2.py` keeps the original script as its base but improves condition verbalization:

- top-level conjunctions are verbalized as `all of the following hold`
- disjunctions are verbalized with `either ... or ...`
- conjunctions inside disjunction branches are verbalized with `both ... and ...`
- all V2 outputs are written to `outputs/roundtrip_v2/`

## Generated Files

- `roundtrip_backtranslations_v2.csv` and `.json`: ChatGPT baseline V2 backtranslations
- `roundtrip_evaluated_v2.csv` and `.json`: automatic evaluation of ChatGPT baseline V2 backtranslations
- `claude_roundtrip_backtranslations_v2.csv` and `.json`: Claude V2 backtranslations
- `claude_roundtrip_evaluated_v2.csv` and `.json`: automatic evaluation of Claude V2 backtranslations

## Automatic Evaluation Counts

- ChatGPT baseline V2: score 2 = 540, score 1 = 38, score 0 = 22
- Claude V2: score 2 = 582, score 1 = 14, score 0 = 4

These V2 outputs should be treated as an additional analysis layer, not as a replacement for the original round-trip results.
