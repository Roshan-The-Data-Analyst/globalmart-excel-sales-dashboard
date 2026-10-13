# GlobalMart Sales Dashboard — Excel E-commerce Analytics

An interactive Excel dashboard project based on a **simulated** e-commerce dataset covering Sri Lanka, the UAE, and Oman from 1 January 2023 through 31 December 2025. It demonstrates data validation, KPI design, PivotTables, PivotCharts, Power Query workflows, and decision-focused analysis.

![GlobalMart dashboard preview](screenshots/dashboard-preview.png)

## Executive summary

| KPI | Verified result |
|---|---:|
| Order records | 15,150 |
| Unique customers | 3,173 |
| Gross sales | 5,004,016.22 |
| Discounts | 384,831.78 |
| Net sales | 4,619,184.44 |
| Weighted discount rate | 7.69% |
| Average order value | 304.90 |
| Returned orders | 879 (5.80%) |
| Average rating | 4.14 / 5 |
| Average delivery time | 5.51 days |

**Important:** The dataset has no currency field or currency code. Monetary amounts above are in **unspecified dataset units**, not a claimed real-world currency. Do not compare country totals as currency-safe measures until currency treatment is confirmed. The data is simulated and must not be presented as actual company performance.

## Key findings

- **Electronics leads recorded net sales:** 2,811,450.54, or 60.86% of the dataset total. Monitor concentration alongside availability, return rates, and actual margin data.
- **Country totals:** Sri Lanka records 2,086,536.22 (45.17%), UAE 1,572,152.78 (34.04%), Oman 960,495.44 (20.79%). These are source-unit shares only because currency is not provided.
- **Mobile App leads the channels:** 2,137,418.69 (46.27%); Website accounts for 39.10% and Marketplace for 14.62%.
- **Marketplace has the highest observed channel return rate:** 6.57%, versus 5.80% overall. Treat this as an investigation signal, not causation.
- **Product return watchlist:** T-Shirt 8.07% (33/409), Lamp 7.85% (39/497), Cooking Oil 7.66% (49/640). Return reasons are missing, so causes cannot be inferred.
- **Annual net sales fell in 2024 and were almost unchanged in 2025:** 1,615,693.86 in 2023; 1,501,828.38 in 2024 (-7.05%); 1,501,662.20 in 2025 (-0.01%). This describes the observed trend but does not explain why it occurred.

See [verified analysis](docs/verified-analysis.md), [business recommendations](docs/business-recommendations.md), and [generated reports](reports/).

## Data validation

The raw CSV contains 15,150 rows and 19 columns. Checks found no missing cells, exact duplicate rows, repeated OrderID values, invalid date strings, or invalid numeric entries in audited fields. GrossSales reconciles to Quantity × UnitPrice at cent precision, and NetSales reconciles to GrossSales − DiscountAmount.

A conventional half-up calculation of DiscountAmount differs by one cent on 368 rows, with no differences larger than one cent. Confirm the source rounding rule before changing values. These checks do not prove that all source business rules are correct or that the data is real.

## Project contents

- [Excel workbook](workbook/GlobalMart_Sales_Dashboard_and_Cleaned_Data.xlsx)
- [Raw CSV dataset](data/raw/globalmart_dataset_raw.csv)
- [Dashboard preview](screenshots/dashboard-preview.png)
- [KPI summary](reports/kpi_summary.csv)
- [Annual sales](reports/annual_sales.csv)
- [Monthly sales](reports/monthly_sales.csv)
- [Country performance](reports/country_performance.csv)
- [Category performance](reports/category_performance.csv)
- [Channel performance](reports/channel_performance.csv)
- [Product return watchlist](reports/product_returns.csv)
- [Quality audit JSON](reports/data_quality_audit.json)
- [Data dictionary](docs/data-dictionary.md)

## Reproduce the analysis

Requires Python 3.10+; the script uses only the standard library:

```bash
python scripts/analyze_sales.py
```

Optional input/output paths:

```bash
python scripts/analyze_sales.py --input data/raw/globalmart_dataset_raw.csv --output-dir reports
```

## Next improvements

1. Add currency codes and a consistent conversion policy before regional value comparisons.
2. Capture return reasons, product condition, and service-level context.
3. Include cost fields before evaluating profitability.
4. Track proposed operational changes against a baseline and review date.

## Skills demonstrated

Microsoft Excel, PivotTables, PivotCharts, slicers, Power Query, data-quality validation, KPI definition, descriptive analysis, Python, and business communication.
