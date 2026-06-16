# Thesis Parser Project

This repository contains the dataset, prompts, grammar, scripts, and derived outputs for the normative food recommendation case study.

## Repository Choice

Use one repository for this work:

- `llm-normative-recommender`

The thesis parser folder can live inside that repository as the project implementation folder. Separate repositories are not needed because the prompts, datasets, parser, ASTs, and round-trip outputs are all parts of the same reproducible pipeline.

## Folder Structure

```text
thesisparser/
├── README.md
├── data/
│   ├── revised/
│   │   ├── user_dataset.csv
│   │   ├── food_ministry_dataset.csv
│   │   ├── food_industry_dataset.csv
│   │   └── constitutive_rules.csv
│   ├── pilot/
│   │   ├── pilot_user.csv
│   │   ├── pilot_food_ministry.csv
│   │   ├── pilot_food_industry.csv
│   │   └── pilot_constitutive_rules.csv
│   └── legacy/
│       ├── user_dataset.csv
│       ├── food_ministry_dataset.csv
│       └── food_industry_dataset.csv
├── docs/
│   ├── thesis_draft.md
│   ├── thesis_draft_dj4me.md
│   ├── thesiscontext.md
│   ├── literature_links.md
│   ├── literature_review_notes.md
│   └── revised_formula_patterns.md
├── grammar/
│   └── grammar.lark
├── outputs/
│   ├── asts/
│   │   ├── revised_user_asts.json
│   │   ├── revised_food_ministry_asts.json
│   │   ├── revised_food_industry_asts.json
│   │   └── constitutive_rule_asts.json
│   └── roundtrip/
│       ├── roundtrip_backtranslations.csv
│       ├── roundtrip_backtranslations.json
│       ├── roundtrip_evaluated.csv
│       └── roundtrip_evaluated.json
├── prompts/
│   ├── prompt_user.md
│   ├── prompt_food_ministry.md
│   ├── prompt_food_industry.md
│   └── prompt_constitutive_rules.md
└── scripts/
    ├── parser.py
    ├── validate_revised_datasets.py
    ├── generate_revised_user_dataset.py
    ├── generate_revised_food_ministry_dataset.py
    ├── generate_revised_food_industry_dataset.py
    ├── generate_constitutive_rules.py
    ├── generate_asts.py
    ├── backtranslate_roundtrip.py
    ├── evaluate_roundtrip.py
    └── generate_stakeholder_datasets.py
```

## Main Files

- `grammar/grammar.lark`: fixed modal/deontic FOL grammar used for validation and AST generation.
- `prompts/`: reproducible prompts for generating stakeholder-specific datasets.
- `data/revised/`: main revised datasets addressing the supervisor comments.
- `data/pilot/`: small pilot examples used before the full revised datasets.
- `data/legacy/`: older datasets kept only for comparison/history.
- `outputs/asts/`: AST JSON outputs generated from the revised datasets.
- `outputs/roundtrip/`: formal-logic-to-natural-language backtranslations and evaluation files.
- `docs/`: thesis draft, DJ4ME framing, literature notes, and design notes.

## Reproducible Pipeline

Run these commands from the `thesisparser` folder:

```bash
python scripts/generate_revised_user_dataset.py
python scripts/generate_revised_food_ministry_dataset.py
python scripts/generate_revised_food_industry_dataset.py
python scripts/generate_constitutive_rules.py
python scripts/validate_revised_datasets.py
python scripts/generate_asts.py
python scripts/backtranslate_roundtrip.py
python scripts/evaluate_roundtrip.py
```

## Current Dataset Design

The revised stakeholder datasets use this schema:

```text
id, stakeholder, nl_norm, implication_formula, dyadic_formula, norm_type
```

Each natural-language norm is paired with both:

- an implication-based monadic formulation, such as `X->O(Y)`
- a dyadic formulation, such as `O(Y|X)`

The constitutive rules dataset uses this schema:

```text
id, scope, nl_rule, logic_rule, category
```

Constitutive rules are kept separate from stakeholder norms because they represent background domain knowledge rather than obligations, permissions, or prohibitions.

## Verification Status

The current revised datasets validate successfully:

```text
data/revised/user_dataset.csv: rows=100 formulas=200 errors=0 warnings=0
data/revised/food_ministry_dataset.csv: rows=100 formulas=200 errors=0 warnings=0
data/revised/food_industry_dataset.csv: rows=100 formulas=200 errors=0 warnings=0
data/revised/constitutive_rules.csv: rows=50 formulas=50 errors=0 warnings=0
TOTAL: rows=350 formulas=650 errors=0 warnings=0
VALIDATION PASSED
```

AST and round-trip outputs were also regenerated:

```text
TOTAL AST RECORDS: 350
roundtrip rows=600
evaluated rows=600
auto score counts={'2': 538, '1': 40, '0': 22}
```
