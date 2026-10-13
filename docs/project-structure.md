# Project Organization Guide

Use this layout as the project evolves. Keep the current workbook and source files in place until you have confirmed their purpose and updated any links.

```text
globalmart-excel-sales-dashboard/
├── README.md
├── data/
│   ├── raw/                 # Original dataset; share only if permitted
│   └── processed/           # Cleaned, reproducible outputs
├── workbook/                # Main Excel workbook
├── screenshots/             # Dashboard previews for documentation
├── docs/
│   ├── project-structure.md
│   ├── data-dictionary.md
│   └── analysis-notes.md
└── .gitignore
```

## What belongs where?

- **data/raw/** — original dataset, with source and license notes.
- **data/processed/** — cleaned datasets used by the workbook; document transformations.
- **workbook/** — the main `.xlsx` workbook and any essential supporting workbook files.
- **screenshots/** — optimized PNG/JPG screenshots used in the README.
- **docs/data-dictionary.md** — column names, definitions, units, and example values.
- **docs/analysis-notes.md** — validated KPIs, findings, caveats, and recommendations.

## Organization checklist

- [ ] Identify the authoritative workbook and dataset.
- [ ] Check that the workbook opens and slicers/charts still work.
- [ ] Keep only useful deliverables; avoid duplicate exports and temporary files.
- [ ] Document the dataset source, reporting period, and metric definitions.
- [ ] Replace placeholder findings with values verified against the workbook.
- [ ] Confirm that data can legally and safely be published before committing it.

This guide describes the recommended future layout; it does not claim that all listed folders or files already exist.
