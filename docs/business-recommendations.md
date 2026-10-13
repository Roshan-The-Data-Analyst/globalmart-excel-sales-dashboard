# Business Recommendations

These are evidence-led hypotheses for a simulated-data portfolio case study, not claims about an actual retailer.

## 1. Confirm currency comparability before regional decisions

**Evidence:** Sri Lanka accounts for 45.17%, UAE 34.04%, and Oman 20.79% of recorded net sales, but the source has no currency code.

**Action:** Add transaction currency, source, and exchange-rate date/rate; publish normalized reporting-currency totals while keeping local amounts traceable.

**Measure:** Transactions with valid currency metadata and reconciliation difference between local and reporting totals.

**Priority:** Highest, because a currency mismatch can make a correct arithmetic comparison misleading.

## 2. Investigate return-rate hotspots

**Evidence:** Overall return rate is 5.80%; Marketplace is 6.57%. T-Shirt is 8.07% (33/409), Lamp 7.85% (39/497), Cooking Oil 7.66% (49/640), and Running Shoes 7.24% (46/635).

**Action:** Add controlled return reasons (sizing/fit, damaged, not as described, compatibility, late delivery, buyer changed mind), then compare by SKU, channel, and country. Audit a sample of returns.

**Measure:** Return rate by reason/product/channel and return cost when available.

**Caution:** Observed differences do not identify causes; do not claim defects or channel causation without return-reason evidence.

## 3. Protect the electronics sales base while validating unit economics

**Evidence:** Electronics contributes 2,811,450.54 in recorded net sales (60.86%). Speaker and Smartwatch are the largest products by recorded net sales.

**Action:** Monitor availability, SKU returns, pricing, and replenishment. Add cost of goods, fulfilment costs, and promotional costs before prioritizing spend.

**Measure:** In-stock rate, net sales, return rate, and gross margin once cost data is available.

**Caution:** Net sales share is not profit share; cost data is absent.

## 4. Diagnose the 2024 net-sales step-down

**Evidence:** Net sales were 1,615,693.86 in 2023, 1,501,828.38 in 2024 (-7.05%), and 1,501,662.20 in 2025 (-0.01%). Orders were 5,105, 5,028, and 5,017; average order value was 316.49, 298.69, and 299.31.

**Action:** Decompose changes by month, category, product, country, order volume, average order value, and discount mix. Validate date and currency comparability first, then test a specific intervention against a baseline.

**Measure:** Monthly net sales, distinct orders, AOV, discount rate, and category mix.

**Caution:** The trend shows what changed, not why.

## 5. Standardize discount rounding and define a service-level measure

**Evidence:** 368 discounts are one cent different from conventional half-up calculation; none is more than one cent. Average delivery is 5.51 days and rating is 4.14/5; 80.34% of ratings are 4 or 5.

**Action:** Document the discount formula and rounding point. Define an explicit delivery SLA and track late deliveries and rating distributions.

**Measure:** Reconciliation exceptions, on-time delivery rate, delivery percentiles, and rating distribution.

**Caution:** An average duration alone cannot be called good or bad without a promised-delivery target.

## Suggested order

1. Add currency and document monetary formulas.
2. Capture return reasons and cost fields.
3. Validate workbook totals against reproducible output.
4. Investigate SKU/channel return patterns.
5. Measure intervention outcomes against a baseline.
