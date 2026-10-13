# Project Structure Guide

The repository groups files by purpose:

- `data/raw/` — original source dataset. Preserve this as the source of truth.
- `workbook/` — primary Excel dashboard and cleaned data.
- `screenshots/dashboard-preview.png` — main preview displayed by the README.
- `screenshots/dashboards/` — other dashboard screenshots.
- `screenshots/data-cleaning/` — screenshots documenting data-cleaning steps.
- `screenshots/insights/` — KPI and analysis chart screenshots.
- `docs/` — project documentation, data definitions, and validated findings.

## Maintenance checklist

- Keep original data separate from processed outputs.
- Avoid uploading temporary Office files and duplicate exports.
- Verify the workbook still opens and slicers/charts work after local changes.
- Update README links if any filenames or folders change.
- Document data provenance and sharing restrictions before publishing source data.
- Validate every numerical insight before adding it to the README.
