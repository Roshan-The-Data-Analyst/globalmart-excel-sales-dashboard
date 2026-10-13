# Analysis Notes

Regenerate reports from `data/raw/globalmart_dataset_raw.csv`:

```bash
python scripts/analyze_sales.py
```

Outputs include KPI, annual/monthly sales, country/category/channel, product-return reports, and a JSON quality audit.

- **Order count:** distinct OrderID values.
- **Net sales:** sum of NetSales.
- **Average order value:** NetSales / distinct orders.
- **Weighted discount rate:** sum of DiscountAmount / sum of GrossSales.
- **Return rate:** distinct orders marked Returned=Yes / distinct orders.
- **Average rating:** mean of Rating.
- **Average delivery:** mean of DeliveryDays.

Interpretation rules: label the dataset as simulated; do not assign a currency symbol; distinguish weighted discount from mean DiscountPct; do not infer causality; do not claim profit without cost data. See [verified analysis](verified-analysis.md) and [business recommendations](business-recommendations.md).
