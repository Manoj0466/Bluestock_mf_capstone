from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///bluestock_mf.db")

fund = pd.read_csv("Processed data/clean_fund_master.csv")
nav = pd.read_csv("Processed data/clean_nav_history.csv")
tx = pd.read_csv("Processed data/clean_investor_transactions.csv")
perf = pd.read_csv("Processed data/clean_scheme_performance.csv")

fund.to_sql("dim_fund", engine, if_exists="replace", index=False)
nav.to_sql("fact_nav", engine, if_exists="replace", index=False)
tx.to_sql("fact_transactions", engine, if_exists="replace", index=False)
perf.to_sql("fact_performance", engine, if_exists="replace", index=False)

print("Database Loaded Successfully")