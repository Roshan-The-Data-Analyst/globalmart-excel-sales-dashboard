# Project Structure Guide

```text
globalmart-excel-sales-dashboard/
├── README.md
├── data/raw/globalmart_dataset_raw.csv
├── workbook/GlobalMart_Sales_Dashboard_and_Cleaned_Data.xlsx
├── screenshots/
├── scripts/analyze_sales.py
├── reports/
│   ├── kpi_summary.csv
│   ├── annual_sales.csv
│   ├── monthly_sales.csv
│   ├── country_performance.csv
│   ├── category_performance.csv
│   ├── channel_performance.csv
│   ├── product_returns.csv
│   └── data_quality_audit.json
└── docs/
    ├── project-structure.md
    ├── data-dictionary.md
    ├── analysis-notes.md
    ├── verified-analysis.md
    └── business-recommendations.md
```

Run `python scripts/analyze_sales.py` from the repository root to regenerate reports. Keep raw data unchanged, verify currency and rounding policies, and validate changes to workbook charts/slicers before publishing.
