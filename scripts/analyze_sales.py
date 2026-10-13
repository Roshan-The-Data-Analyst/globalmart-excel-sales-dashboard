#!/usr/bin/env python3
"""Generate reproducible GlobalMart sales summaries and a data-quality audit using stdlib only."""
from __future__ import annotations
import argparse, csv, json
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

D=Decimal
CENT=D("0.01")
ZERO=D("0")
REQUIRED=["OrderID","OrderDate","Country","City","Category","Product","Quantity","UnitPrice","DiscountPct","DiscountAmount","GrossSales","NetSales","PaymentMethod","Channel","CustomerSegment","CustomerID","DeliveryDays","Returned","Rating"]
NUMERIC=["Quantity","UnitPrice","DiscountPct","DiscountAmount","GrossSales","NetSales","DeliveryDays","Rating"]

def dec(row, field):
    return D(row[field].strip())
def money(x):
    return x.quantize(CENT,rounding=ROUND_HALF_UP)
def fmt(x):
    return f"{D(str(x)).quantize(CENT,rounding=ROUND_HALF_UP):.2f}"
def pct(x):
    return fmt(x*D("100"))
def total(rows, field):
    return sum((dec(r,field) for r in rows),ZERO)
def distinct(rows, field):
    return len({r[field].strip() for r in rows})
def write_csv(path, fields, records):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(records)
def load(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f);headers=reader.fieldnames or []
        missing=[k for k in REQUIRED if k not in headers]
        if missing: raise ValueError("Missing required columns: "+", ".join(missing))
        rows=[r for r in reader if any((v or "").strip() for v in r.values())]
    if not rows: raise ValueError("No transaction rows in source CSV.")
    return rows,headers
def aggregate(rows, dimension):
    group=defaultdict(list)
    for r in rows: group[r[dimension].strip()].append(r)
    net_all=total(rows,"NetSales");out=[]
    for name,items in group.items():
        order_n=distinct(items,"OrderID")
        returns=distinct([r for r in items if r["Returned"].strip().casefold()=="yes"],"OrderID")
        net=total(items,"NetSales")
        out.append({"name":name,"orders":order_n,"net_sales":net,"sales_share":net/net_all if net_all else ZERO,
          "average_order_value":net/D(order_n),"returned_orders":returns,"return_rate":D(returns)/D(order_n),
          "avg_discount_pct":total(items,"DiscountPct")/D(len(items)),
          "avg_delivery_days":total(items,"DeliveryDays")/D(len(items)),
          "average_rating":total(items,"Rating")/D(len(items))})
    return out
def audit_data(rows,headers):
    missing={k:sum(not (r.get(k) or "").strip() for r in rows) for k in headers}
    signatures=Counter(tuple((r.get(k) or "").strip() for k in headers) for r in rows)
    exact_duplicates=sum(n-1 for n in signatures.values() if n>1)
    order_counts=Counter(r["OrderID"].strip() for r in rows)
    dates=[];bad_dates=0
    for r in rows:
        try: dates.append(date.fromisoformat(r["OrderDate"].strip()).isoformat())
        except ValueError: bad_dates+=1
    numeric_bad={};ranges={}
    for key in NUMERIC:
        values=[];bad=0
        for r in rows:
            try: values.append(dec(r,key))
            except Exception: bad+=1
        numeric_bad[key]=bad;ranges[key]={"min":str(min(values)) if values else None,"max":str(max(values)) if values else None}
    city_country=defaultdict(set);product_category=defaultdict(set)
    gross_bad=net_bad=discount_exact=discount_one=discount_more=max_cents=0
    for r in rows:
        city_country[r["City"].strip()].add(r["Country"].strip())
        product_category[r["Product"].strip()].add(r["Category"].strip())
        quantity,price=dec(r,"Quantity"),dec(r,"UnitPrice")
        gross,discount,net=dec(r,"GrossSales"),dec(r,"DiscountAmount"),dec(r,"NetSales")
        if money(quantity*price)!=money(gross): gross_bad+=1
        if money(gross-discount)!=money(net): net_bad+=1
        expected=money(gross*dec(r,"DiscountPct")/D("100"))
        cents_diff=int(abs(discount-expected)/CENT);max_cents=max(max_cents,cents_diff)
        if cents_diff==0: discount_exact+=1
        elif cents_diff==1: discount_one+=1
        else: discount_more+=1
    ranges_bad={
      "Quantity":sum(not (D("1")<=dec(r,"Quantity")<=D("5")) for r in rows),
      "UnitPrice":sum(dec(r,"UnitPrice")<=ZERO for r in rows),
      "DiscountPct":sum(not (ZERO<=dec(r,"DiscountPct")<=D("100")) for r in rows),
      "DiscountAmount":sum(dec(r,"DiscountAmount")<ZERO for r in rows),
      "GrossSales":sum(dec(r,"GrossSales")<ZERO for r in rows),
      "NetSales":sum(dec(r,"NetSales")<ZERO for r in rows),
      "DeliveryDays":sum(dec(r,"DeliveryDays")<ZERO for r in rows),
      "Rating":sum(not (D("1")<=dec(r,"Rating")<=D("5")) for r in rows),
      "Returned":sum(r["Returned"].strip().casefold() not in {"yes","no"} for r in rows)}
    return {"source":"data/raw/globalmart_dataset_raw.csv","dataset_type":"Simulated e-commerce data, per project description",
      "row_count":len(rows),"column_count":len(headers),"columns":headers,
      "date_range":{"min":min(dates) if dates else None,"max":max(dates) if dates else None},
      "missing_values_by_column":missing,"total_missing_cells":sum(missing.values()),
      "exact_duplicate_rows":exact_duplicates,"distinct_order_ids":len(order_counts),
      "duplicate_order_id_occurrences":sum(n-1 for n in order_counts.values() if n>1),
      "distinct_customer_ids":distinct(rows,"CustomerID"),"invalid_date_rows":bad_dates,
      "invalid_numeric_values_by_column":numeric_bad,"observed_numeric_ranges":ranges,"range_violations":ranges_bad,
      "dimensions":{"countries":distinct(rows,"Country"),"cities":distinct(rows,"City"),"categories":distinct(rows,"Category"),
        "products":distinct(rows,"Product"),"channels":distinct(rows,"Channel"),"payment_methods":distinct(rows,"PaymentMethod"),
        "customer_segments":distinct(rows,"CustomerSegment")},
      "city_country_conflicts":[{"city":k,"countries":sorted(v)} for k,v in city_country.items() if len(v)>1],
      "product_category_conflicts":[{"product":k,"categories":sorted(v)} for k,v in product_category.items() if len(v)>1],
      "currency_field_present":any("currency" in k.casefold() for k in headers),
      "formula_validation":{"gross_sales_formula_mismatches":gross_bad,"net_sales_formula_mismatches":net_bad,
        "discount_amount_vs_conventional_half_up_rounding":{"exact_matches":discount_exact,"one_cent_differences":discount_one,
          "over_one_cent_differences":discount_more,"max_difference_cents":max_cents}},
      "caveats":["No currency field or currency code exists; amounts are unspecified dataset units.",
        "The project describes this dataset as simulated.",
        "Some discounts differ by one cent from conventional half-up rounding; confirm source policy before changing values."]}
def main():
    root=Path(__file__).resolve().parents[1]
    p=argparse.ArgumentParser(description="Generate GlobalMart KPI reports and quality checks.")
    p.add_argument("--input",type=Path,default=root/"data"/"raw"/"globalmart_dataset_raw.csv")
    p.add_argument("--output-dir",type=Path,default=root/"reports")
    args=p.parse_args();rows,headers=load(args.input);out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    a=audit_data(rows,headers)
    gross,discount,net=total(rows,"GrossSales"),total(rows,"DiscountAmount"),total(rows,"NetSales")
    n_orders,n_customers=distinct(rows,"OrderID"),distinct(rows,"CustomerID")
    n_return=distinct([r for r in rows if r["Returned"].strip().casefold()=="yes"],"OrderID")
    wdisc=discount/gross; avgdisc=total(rows,"DiscountPct")/D(len(rows))/D("100")
    rating=total(rows,"Rating")/D(len(rows)); delivery=total(rows,"DeliveryDays")/D(len(rows));qty=total(rows,"Quantity")/D(len(rows))
    r4=sum(dec(r,"Rating")>=D("4") for r in rows)
    kpis=[
      {"metric":"Order count","value":str(n_orders),"definition":"Distinct OrderID values; one row per order in this source."},
      {"metric":"Unique customers","value":str(n_customers),"definition":"Distinct CustomerID values."},
      {"metric":"Date range","value":f'{a["date_range"]["min"]} to {a["date_range"]["max"]}',"definition":"Minimum and maximum OrderDate values."},
      {"metric":"Gross sales","value":fmt(gross),"definition":"Sum of GrossSales; currency unspecified."},
      {"metric":"Discount amount","value":fmt(discount),"definition":"Sum of DiscountAmount."},
      {"metric":"Net sales","value":fmt(net),"definition":"Sum of NetSales; currency unspecified."},
      {"metric":"Weighted discount rate (%)","value":pct(wdisc),"definition":"Sum of DiscountAmount / sum of GrossSales."},
      {"metric":"Average row discount (%)","value":pct(avgdisc),"definition":"Mean DiscountPct; not a weighted discount rate."},
      {"metric":"Average order value","value":fmt(net/D(n_orders)),"definition":"Net sales / distinct order count; currency unspecified."},
      {"metric":"Returned orders","value":str(n_return),"definition":"Distinct OrderID values with Returned=Yes."},
      {"metric":"Return rate (%)","value":pct(D(n_return)/D(n_orders)),"definition":"Returned orders / distinct orders."},
      {"metric":"Average rating (out of 5)","value":fmt(rating),"definition":"Arithmetic mean of Rating."},
      {"metric":"Average delivery days","value":fmt(delivery),"definition":"Arithmetic mean of DeliveryDays."},
      {"metric":"Average quantity per order","value":fmt(qty),"definition":"Arithmetic mean of Quantity."},
      {"metric":"Orders rated 4 or 5 (%)","value":pct(D(r4)/D(len(rows))),"definition":"Share of records with Rating >= 4."}]
    write_csv(out/"kpi_summary.csv",["metric","value","definition"],kpis)
    years=defaultdict(list);months=defaultdict(list)
    for r in rows: years[r["OrderDate"][:4]].append(r);months[r["OrderDate"][:7]].append(r)
    annual=[];prior=None
    for year in sorted(years):
        rr=years[year];n=distinct(rr,"OrderID");ret=distinct([r for r in rr if r["Returned"].strip().casefold()=="yes"],"OrderID");ns=total(rr,"NetSales")
        annual.append({"year":year,"orders":n,"gross_sales":fmt(total(rr,"GrossSales")),"discount_amount":fmt(total(rr,"DiscountAmount")),
          "net_sales":fmt(ns),"average_order_value":fmt(ns/D(n)),"returned_orders":ret,"return_rate_pct":pct(D(ret)/D(n)),
          "yoy_net_sales_change_pct":"" if prior is None else pct(ns/prior-D("1"))})
        prior=ns
    write_csv(out/"annual_sales.csv",["year","orders","gross_sales","discount_amount","net_sales","average_order_value","returned_orders","return_rate_pct","yoy_net_sales_change_pct"],annual)
    monthly=[]
    for month in sorted(months):
        rr=months[month];n=distinct(rr,"OrderID");ret=distinct([r for r in rr if r["Returned"].strip().casefold()=="yes"],"OrderID")
        monthly.append({"month":month,"orders":n,"net_sales":fmt(total(rr,"NetSales")),"average_order_value":fmt(total(rr,"NetSales")/D(n)),
          "returned_orders":ret,"return_rate_pct":pct(D(ret)/D(n)),"avg_rating":fmt(total(rr,"Rating")/D(len(rr)))})
    write_csv(out/"monthly_sales.csv",["month","orders","net_sales","average_order_value","returned_orders","return_rate_pct","avg_rating"],monthly)
    cols=["name","orders","net_sales","sales_share_pct","average_order_value","returned_orders","return_rate_pct","avg_discount_pct","avg_delivery_days","average_rating"]
    for dimension,filename in [("Country","country_performance.csv"),("Category","category_performance.csv"),("Channel","channel_performance.csv")]:
        gs=sorted(aggregate(rows,dimension),key=lambda x:x["net_sales"],reverse=True)
        out_rows=[{"name":g["name"],"orders":g["orders"],"net_sales":fmt(g["net_sales"]),"sales_share_pct":pct(g["sales_share"]),
          "average_order_value":fmt(g["average_order_value"]),"returned_orders":g["returned_orders"],"return_rate_pct":pct(g["return_rate"]),
          "avg_discount_pct":fmt(g["avg_discount_pct"]),"avg_delivery_days":fmt(g["avg_delivery_days"]),"average_rating":fmt(g["average_rating"])} for g in gs]
        write_csv(out/filename,cols,out_rows)
    products=sorted(aggregate(rows,"Product"),key=lambda x:(x["return_rate"],x["net_sales"]),reverse=True)
    product_rows=[{"product":g["name"],"orders":g["orders"],"returned_orders":g["returned_orders"],"return_rate_pct":pct(g["return_rate"]),
      "net_sales":fmt(g["net_sales"]),"sales_share_pct":pct(g["sales_share"]),"average_rating":fmt(g["average_rating"]),
      "average_order_value":fmt(g["average_order_value"])} for g in products]
    write_csv(out/"product_returns.csv",["product","orders","returned_orders","return_rate_pct","net_sales","sales_share_pct","average_rating","average_order_value"],product_rows)
    a["monetary_unit_note"]="No currency column exists; monetary values are in unspecified dataset units."
    a["kpis"]={"orders":n_orders,"unique_customers":n_customers,"gross_sales":fmt(gross),"discount_amount":fmt(discount),"net_sales":fmt(net),
      "weighted_discount_rate_pct":pct(wdisc),"average_row_discount_pct":pct(avgdisc),"average_order_value":fmt(net/D(n_orders)),
      "returned_orders":n_return,"return_rate_pct":pct(D(n_return)/D(n_orders)),"average_rating":fmt(rating),"average_delivery_days":fmt(delivery),
      "average_quantity_per_order":fmt(qty),"orders_rated_4_or_5_pct":pct(D(r4)/D(len(rows)))}
    a["annual_sales"]=annual;a["monthly_sales_highest"]=max(monthly,key=lambda x:D(x["net_sales"]));a["monthly_sales_lowest"]=min(monthly,key=lambda x:D(x["net_sales"]))
    a["top_categories_by_net_sales"]=[{"name":g["name"],"orders":g["orders"],"net_sales":fmt(g["net_sales"]),"sales_share_pct":pct(g["sales_share"])} for g in sorted(aggregate(rows,"Category"),key=lambda x:x["net_sales"],reverse=True)[:3]]
    a["top_products_by_net_sales"]=[{"name":g["name"],"orders":g["orders"],"net_sales":fmt(g["net_sales"]),"sales_share_pct":pct(g["sales_share"])} for g in sorted(aggregate(rows,"Product"),key=lambda x:x["net_sales"],reverse=True)[:5]]
    a["top_return_rate_products"]=product_rows[:5]
    a["limitations"]=["The dataset is described as simulated; results are not evidence of real company performance.","No currency field or code exists, so regional monetary comparisons may be invalid if currencies differ.","No cost data is present, so profit and margin cannot be calculated.","Return reasons are absent; high rates identify investigation priorities, not causes."]
    with (out/"data_quality_audit.json").open("w",encoding="utf-8") as f: json.dump(a,f,indent=2,ensure_ascii=False);f.write("\n")
    print(f"Rows: {len(rows):,}; orders: {n_orders:,}; net sales (unspecified units): {fmt(net)}; return rate: {pct(D(n_return)/D(n_orders))}%")
    print(f"Reports written to {out.resolve()}")
if __name__=="__main__": main()
