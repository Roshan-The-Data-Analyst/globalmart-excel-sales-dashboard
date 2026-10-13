# Data Dictionary

Source: `data/raw/globalmart_dataset_raw.csv`. The dataset has 15,150 records and 19 columns and covers 2023-01-01 to 2025-12-31. Project documentation describes it as simulated.

| Column | Meaning | Validation notes |
|---|---|---|
| OrderID | Order identifier | 15,150 unique values; one row per order |
| OrderDate | Order date | YYYY-MM-DD |
| Country | Country/market | Sri Lanka, UAE, Oman |
| City | City | 13 cities; each maps to one country here |
| Category | Product category | Six categories |
| Product | Product name | 29 products; one category per product in this data |
| Quantity | Units in the order | Integer values 1–5 |
| UnitPrice | Price per unit | Monetary currency unspecified |
| DiscountPct | Discount rate | Values: 0, 5, 10, 15, 20, 25 |
| DiscountAmount | Discount value | Currency unspecified; cent rounding convention needs documentation |
| GrossSales | Value before discount | Reconciles with Quantity × UnitPrice at cent precision |
| NetSales | Value after discount | Reconciles with GrossSales − DiscountAmount at cent precision |
| PaymentMethod | Payment method | Five methods |
| Channel | Sales channel | Mobile App, Website, Marketplace |
| CustomerSegment | Customer segment | New, Returning, VIP |
| CustomerID | Customer identifier | 3,173 distinct IDs |
| DeliveryDays | Delivery duration | Integer 1–10 |
| Returned | Return flag | Yes / No |
| Rating | Customer rating | Integer 1–5 |

## Limits

- No currency field exists; monetary outputs are unspecified dataset units.
- Cost, shipping-cost, and marketing-spend data are absent; profit/margin cannot be computed.
- Return-reason data is absent; product and channel return differences do not explain their causes.
- The project should label results as simulated-data analysis.
- Some discounts differ by one cent from a conventional half-up calculation. Confirm the source rule; do not silently overwrite values.
