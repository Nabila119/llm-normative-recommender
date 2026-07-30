# Claude Human Round-Trip Evaluation Summary

This summary reports manually reviewed Claude round-trip rows. The reviewed set includes all rows whose automatic semantic score was 0 or 1, plus a reproducible 50-row sample from rows whose automatic semantic score was 2.

## Overall

- Total Claude round-trip rows: 600
- Human-reviewed rows: 100
- Human score 2: 61
- Human score 1: 37
- Human score 0: 2
- Auto-human exact agreement on reviewed rows: 81/100 (81.0%)

## Reviewed Set Composition

- Auto score 0 rows in reviewed set: 4
- Auto score 1 rows in reviewed set: 46
- Auto score 2 rows in reviewed set: 50

## Auto vs Human Crosstab

| Auto score | Human 0 | Human 1 | Human 2 | Total |
|---|---:|---:|---:|---:|
| Auto 0 | 0 | 0 | 4 | 4 |
| Auto 1 | 2 | 34 | 10 | 46 |
| Auto 2 | 0 | 3 | 47 | 50 |

## Error Types

- missing_condition: 37
- none: 61
- wrong_condition: 2

## By Formula Type

- dyadic: score 2 = 29, score 1 = 20, score 0 = 1
- implication: score 2 = 32, score 1 = 17, score 0 = 1

## By Stakeholder

- Food Industry: score 2 = 14, score 1 = 16, score 0 = 0
- Food Ministry: score 2 = 18, score 1 = 10, score 0 = 0
- User: score 2 = 29, score 1 = 11, score 0 = 2
