import pandas as pd

# print("Loading datasets...")

fund = pd.read_csv("Raw Data/01_fund_master.csv")
nav = pd.read_csv("Raw Data/02_nav_history.csv")
aum = pd.read_csv("Raw Data/03_aum_by_fund_house.csv")
sip = pd.read_csv("Raw Data/04_monthly_sip_inflows.csv")
cat = pd.read_csv("Raw Data/05_category_inflows.csv")
folio = pd.read_csv("Raw Data/06_industry_folio_count.csv")
perf = pd.read_csv("Raw Data/07_scheme_performance.csv")
tx = pd.read_csv("Raw Data/08_investor_transactions.csv")
hold = pd.read_csv("Raw Data/09_portfolio_holdings.csv")
bench = pd.read_csv("Raw Data/10_benchmark_indices.csv")

# print("Datasets loaded successfully")

fund["launch_date"] = pd.to_datetime(fund["launch_date"],format="%d-%m-%Y")

fund.to_csv( "C:/Users/Praneeth Kumar/OneDrive/Desktop/bluestock_mf_capstone/Processed data/clean_fund_master.csv", index=False)

# print("Fund Master Cleaned")

# print(fund["launch_date"].head())

nav["date"] = pd.to_datetime(nav["date"])

nav = nav.sort_values(["amfi_code", "date"])
nav = nav.drop_duplicates()
nav["nav"] = (nav.groupby("amfi_code")["nav"].ffill())
nav = nav[nav["nav"] > 0]
nav["daily_return_pct"] = (nav.groupby("amfi_code")["nav"].pct_change())

nav.to_csv("C:/Users/Praneeth Kumar/OneDrive/Desktop/bluestock_mf_capstone/Processed data/clean_nav_history.csv", index=False)

# print("NAV History Cleaned")

aum["date"] = pd.to_datetime(aum["date"])

aum.to_csv("C:/Users/Praneeth Kumar/OneDrive/Desktop/bluestock_mf_capstone/Processed data/clean_aum_by_fund_house.csv",index=False)

# print("AUM Cleaned")

sip["month"] = pd.to_datetime(sip["month"])

sip["yoy_growth_pct"] = (sip["yoy_growth_pct"] .fillna(0))

sip.to_csv("C:/Users/Praneeth Kumar/OneDrive/Desktop/bluestock_mf_capstone/Processed data/clean_monthly_sip_inflows.csv", index=False)

# print("SIP Data Cleaned")

cat["month"] = pd.to_datetime(cat["month"])

cat.to_csv("C:/Users/Praneeth Kumar/OneDrive/Desktop/bluestock_mf_capstone/Processed data/clean_category_inflows.csv", index=False)

# print("Category Inflows Cleaned")

folio["month"] = pd.to_datetime(folio["month"])

folio.to_csv("C:/Users/Praneeth Kumar/OneDrive/Desktop/bluestock_mf_capstone/Processed data/clean_industry_folio_count.csv", index=False)

# print("Folio Data Cleaned")

return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct", "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio", "sortino_ratio", "std_dev_ann_pct", "max_drawdown_pct"]

for col in return_cols: perf[col] = pd.to_numeric(perf[col],errors="coerce")

perf["negative_sharpe_flag"] = (perf["sharpe_ratio"] < 0)

invalid_expense = perf[(perf["expense_ratio_pct"] < 0.1) | (perf["expense_ratio_pct"] > 2.5)]

perf.to_csv( "C:/Users/Praneeth Kumar/OneDrive/Desktop/bluestock_mf_capstone/Processed data/clean_scheme_performance.csv",index=False)

# print("Performance Data Cleaned")

tx["transaction_date"] = pd.to_datetime(tx["transaction_date"])

tx["transaction_type"] = (tx["transaction_type"].str.strip().str.title())

valid_types = ["Sip", "Lumpsum", "Redemption"]

tx = tx[tx["transaction_type"].isin(valid_types)]

tx = tx[tx["amount_inr"] > 0]

tx["kyc_status"] = (tx["kyc_status"] .str.strip().str.title())

tx.to_csv("C:/Users/Praneeth Kumar/OneDrive/Desktop/bluestock_mf_capstone/Processed data/clean_investor_transactions.csv", index=False)

# print("Transactions Cleaned")

hold["portfolio_date"] = pd.to_datetime(hold["portfolio_date"])

hold.to_csv("C:/Users/Praneeth Kumar/OneDrive/Desktop/bluestock_mf_capstone/Processed data/clean_portfolio_holdings.csv", index=False)

# print("Holdings Cleaned")

bench["date"] = pd.to_datetime(bench["date"])

bench.to_csv("C:/Users/Praneeth Kumar/OneDrive/Desktop/bluestock_mf_capstone/Processed data/clean_benchmark_indices.csv", index=False)

# print("Benchmark Data Cleaned")

