import pandas as pd

df = pd.read_csv("Raw Data/04_monthly_sip_inflows.csv")


# files = [
#     "01_fund_master.csv",
#     "02_nav_history.csv",
#     "03_aum_by_fund_house.csv",
#     "04_monthly_sip_inflows.csv",
#     "05_category_inflows.csv",
#     "06_industry_folio_count.csv",
#     "07_scheme_performance.csv",
#     "08_investor_transactions.csv",
#     "09_portfolio_holdings.csv",
#     "10_benchmark_indices.csv"
# ]

# base_path = r"C:/Users/Praneeth Kumar/OneDrive\Desktop/bluestock_mf_capstone/Raw Data"

# for file in files:
#     print("=" * 60)
#     print("Reading:", file)

#     df = pd.read_csv(f"{base_path}//{file}")

# print("\n")
# print(df.head())
# print(df)
print(df.shape)
# print(df.dtypes)
print(df.isnull().sum())
# print(df["fund_house"].unique())
# print(df["category"].unique())
# print(df["sub_category"].unique())
# print(df["risk_category"].unique())

# fund = pd.read_csv(r"Raw Data/01_fund_master.csv")
# nav = pd.read_csv(r"Raw Data/02_nav_history.csv")

# missing = set(fund["amfi_code"]) - set(nav["amfi_code"])

# if len(missing) == 0:
#     print("All AMFI codes are present.")
# else:
#     print("Missing codes:", missing)



