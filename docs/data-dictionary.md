# Data Dictionary

This document records the main fields described for the GlobalMart analysis. Confirm the exact source column names, units, data types, and null-handling rules against the CSV and Excel workbook before using them in a production analysis.

| Field | Working definition | Validation to perform |
|---|---|---|
| Order Date | Date associated with an order or transaction | Confirm source format, timezone assumptions, and reporting period |
| Region | Market or geography for the transaction | Standardize labels; current project description names Sri Lanka, UAE, and Oman |
| Product Category | Category assigned to the product | Check spelling, blank values, and category consistency |
| Quantity | Units associated with the transaction | Confirm numeric type and treatment of negative or return quantities |
| Unit Price | Price per unit | Confirm currency and numeric format |
| Revenue | Revenue measure, potentially derived from quantity and unit price | Verify the workbook formula, discount treatment, returns, and currency rules |
| Customer Segment | Group used to categorize customers | Verify allowed values and missing-value handling |

## General checks

- Confirm each column's exact header from the source file.
- Document any transformations performed in Power Query.
- Record how duplicate rows, missing values, returns, and invalid quantities are handled.
- Verify whether amounts are in one currency or multiple currencies before comparing regions.
- Keep a note of any calculated column formula and ensure it agrees with the workbook.
