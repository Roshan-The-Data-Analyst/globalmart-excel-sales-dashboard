# Verified Analysis and Methodology

## Scope and caveats

Computed from `data/raw/globalmart_dataset_raw.csv`, a 15,150-record source dataset described in this project as simulated. Dates range from **1 January 2023 to 31 December 2025**. Each record has a unique `OrderID`, so record count and distinct order count are equal here.

There is no currency field. Monetary totals are in **unspecified dataset units**. Country value comparisons are not currency-safe until currency is confirmed. This case study does not support real-company, profit/margin, or causal claims.

## KPI definitions

| Metric | Calculation |
|---|---|
| Order count | Distinct OrderID |
| Net sales | Sum of NetSales |
| Average order value | NetSales / distinct orders |
| Weighted discount rate | Sum of DiscountAmount / sum of GrossSales |
| Average row discount | Mean of DiscountPct; differs from weighted discount |
| Return rate | Distinct orders marked Returned=Yes / distinct orders |
| Average rating | Mean of Rating |
| Average delivery time | Mean of DeliveryDays |

## Headline KPIs

| Metric | Result |
|---|---:|
| Orders | 15,150 |
| Unique customers | 3,173 |
| Gross sales | 5,004,016.22 |
| Discount amount | 384,831.78 |
| Net sales | 4,619,184.44 |
| Weighted discount rate | 7.69% |
| Mean order-level discount percentage | 7.79% |
| Average order value | 304.90 |
| Returned orders | 879 |
| Return rate | 5.80% |
| Average rating | 4.14 / 5 |
| Ratings of 4 or 5 | 80.34% |
| Average delivery | 5.51 days |
| Average quantity | 1.93 |

## Category performance

| Category | Orders | Net sales | Share |
|---|---:|---:|---:|
| Electronics | 2,529 | 2,811,450.54 | 60.86% |
| Home & Living | 2,488 | 577,734.72 | 12.51% |
| Sports | 2,500 | 471,917.70 | 10.22% |
| Beauty | 2,531 | 362,744.66 | 7.85% |
| Fashion | 2,564 | 297,424.26 | 6.44% |
| Groceries | 2,538 | 97,912.56 | 2.12% |

Electronics contributes most recorded monetary value despite similar order count to other categories. That reflects price/value mix, not profitability: the dataset has no product cost data.

## Country and channel

| Country | Orders | Net sales | Share |
|---|---:|---:|---:|
| Sri Lanka | 6,854 | 2,086,536.22 | 45.17% |
| UAE | 5,297 | 1,572,152.78 | 34.04% |
| Oman | 2,999 | 960,495.44 | 20.79% |

Treat these monetary country comparisons as source-unit summaries only until currency and conversion policy are confirmed.

| Channel | Orders | Net sales | Share | Return rate |
|---|---:|---:|---:|---:|
| Mobile App | 6,879 | 2,137,418.69 | 46.27% | 5.52% |
| Website | 6,033 | 1,806,303.54 | 39.10% | 5.83% |
| Marketplace | 2,238 | 675,462.21 | 14.62% | 6.57% |

Marketplace's return rate is 0.77 percentage points above the overall rate. This is a diagnostic signal, not evidence that channel causes returns.

## Annual trend

| Year | Orders | Net sales | Average order value | YoY net sales |
|---|---:|---:|---:|---:|
| 2023 | 5,105 | 1,615,693.86 | 316.49 | — |
| 2024 | 5,028 | 1,501,828.38 | 298.69 | -7.05% |
| 2025 | 5,017 | 1,501,662.20 | 299.31 | -0.01% |

Net sales declined in 2024 and were flat in 2025. Average order value fell from 316.49 to 298.69 between 2023 and 2024, while orders moved from 5,105 to 5,028. Track volume, average order value, discounting, and product mix separately; the dataset does not identify the cause. Highest monthly net sales were in August 2023 (163,113.70), and the lowest in April 2024 (104,252.58). One month does not establish seasonality.

## Return-rate watchlist

| Product | Orders | Returned | Rate |
|---|---:|---:|---:|
| T-Shirt | 409 | 33 | 8.07% |
| Lamp | 497 | 39 | 7.85% |
| Cooking Oil | 640 | 49 | 7.66% |
| Running Shoes | 635 | 46 | 7.24% |
| Tablet | 410 | 28 | 6.83% |

Use these as triage candidates. Return reasons, product condition, and fulfilment context are not available to explain why they were returned.

## Quality audit

The automated audit found zero missing cells, exact duplicate rows, repeated OrderIDs, or invalid ISO dates. Numeric fields parsed; city-country and product-category mappings are internally consistent. GrossSales reconciles with Quantity × UnitPrice at cent precision, and NetSales reconciles with GrossSales − DiscountAmount.

Using a conventional half-up discount calculation, 14,782 records match exactly and 368 differ by one cent; none differs by more than one cent. Confirm the source rounding convention rather than silently changing the data.

Run `python scripts/analyze_sales.py` to regenerate the summary CSVs and audit JSON.
