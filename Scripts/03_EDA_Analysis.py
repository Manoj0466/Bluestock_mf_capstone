import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path

plt.style.use("ggplot")
sns.set_theme(style="whitegrid")

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "Processed data"

CHART_DIR = BASE_DIR / "Charts"

CHART_DIR.mkdir(exist_ok=True)

fund = pd.read_csv("Processed data/clean_fund_master.csv")
nav = pd.read_csv("Processed data/clean_nav_history.csv")
aum = pd.read_csv("Processed data/clean_aum_by_fund_house.csv")
sip = pd.read_csv("Processed data/clean_monthly_sip_inflows.csv")
category = pd.read_csv("Processed data/clean_category_inflows.csv")
folio = pd.read_csv("Processed data/clean_industry_folio_count.csv")
performance = pd.read_csv("Processed data/clean_scheme_performance.csv")
transactions = pd.read_csv("Processed data/clean_investor_transactions.csv")
portfolio = pd.read_csv("Processed data/clean_portfolio_holdings.csv")
benchmark = pd.read_csv("Processed data/clean_benchmark_indices.csv")

# print("loaded datasets Successfully")

datasets = {
    "Fund":fund,
    "NAV":nav,
    "AUM":aum,
    "SIP":sip,
    "Category":category,
    "Folio":folio,
    "Performance":performance,
    "Transactions":transactions,
    "Portfolio":portfolio,
    "Benchmark":benchmark
}

# for name,df in datasets.items():
#     print("="*60)
#     print(name)
#     print(df.shape)
#     print(df.info())
#     print(df.describe(include="all"))

nav["date"]=pd.to_datetime(nav["date"])


nav = nav.merge(
        fund[["amfi_code", "scheme_name"]],
        on="amfi_code",
        how="left"
)

fig = px.line(
        nav,
        x="date",
        y="nav",
        color="scheme_name",
        title="Daily NAV Trend of All Mutual Fund Schemes (2022–2026)"
)

fig.add_vrect(
        x0="2023-01-01",
        x1="2023-12-31",
        fillcolor="green",
        opacity=0.12,
        annotation_text="2023 Bull Run",
        annotation_position="top left"
)

fig.add_vrect(
        x0="2024-01-01",
        x1="2024-12-31",
        fillcolor="red",
        opacity=0.12,
        annotation_text="2024 Market Correction",
        annotation_position="top left"
)

fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        xaxis_title="Date",
        yaxis_title="NAV"
)

# fig.show()

# fig.write_image(CHART_DIR/"01_NAV_Trend.png")

aum["date"] = pd.to_datetime(aum["date"])

aum["year"] = aum["date"].dt.year

plt.figure(figsize=(16, 8))

sns.barplot(
    data=aum,
    x="year",
    y="aum_lakh_crore",
    hue="fund_house"
)

plt.title(
    "AUM Growth by Fund House (2022–2025)",
    fontsize=18,
    fontweight="bold"
)

plt.xlabel("Year", fontsize=13)

plt.ylabel("AUM (₹ Lakh Crore)", fontsize=13)


sbi_2025 = aum[
    (aum["fund_house"]=="SBI Mutual Fund") &
    (aum["year"]==2025)
]

if not sbi_2025.empty:

    value = sbi_2025["aum_lakh_crore"].max()

    plt.text(
        3,            
        value+0.2,
        "SBI ₹12.5L Cr",
        color="red",
        fontsize=12,
        fontweight="bold"
    )

plt.legend(
    title="Fund House",
    bbox_to_anchor=(1.02,1),
    loc="upper left"
)

plt.tight_layout()

# plt.savefig(
#     CHART_DIR/"02_AUM_Growth.png",
#     dpi=300
# )

sip["month"] = pd.to_datetime(sip["month"])

fig = px.line(
        sip,
        x="month",
        y="sip_inflow_crore",
        markers=True,
        title="Monthly SIP Inflow Trend (Jan 2022 - Dec 2025)"
)

fig.add_annotation(
        x="2025-12-01",
        y=31002,
        text="₹31,002 Cr (All Time High)",
        showarrow=True,
        arrowhead=2
)

fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        xaxis_title="Month",
        yaxis_title="SIP Inflow (Crore)"
)

# fig.write_image(
#         CHART_DIR/"03_SIP_Trend.png"
# )

pivot = category.pivot_table(
        index="category",
        columns="month",
        values="net_inflow_crore",
        aggfunc="sum"
)

plt.figure(figsize=(15,7))

sns.heatmap(
        pivot,
        cmap="RdYlGn",
        annot=True,
        fmt=".0f"
    )

plt.title("Category Wise Net Inflow Heatmap")

plt.tight_layout()

# plt.savefig(
#         CHART_DIR/"04_Category_Heatmap.png",
#         dpi=300
# )

age = transactions["age_group"].value_counts()

plt.figure(figsize=(8,8))

plt.pie(
        age,
        labels=age.index,
        autopct="%1.1f%%",
        startangle=90
)

plt.title("Investor Age Group Distribution")

plt.tight_layout()

# plt.savefig(
#         CHART_DIR/"05_Age_Distribution.png",
#         dpi=300
# )

transactions["transaction_type"] = (
    transactions["transaction_type"]
    .str.strip()
    .str.upper()
)

sip_transactions = transactions[
    transactions["transaction_type"] == "SIP"
]

plt.figure(figsize=(12,6))

sns.boxplot(
    data=sip_transactions,
    x="age_group",
    y="amount_inr",
    palette="Set2"
)

plt.title(
    "SIP Amount Distribution by Age Group",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Age Group")

plt.ylabel("SIP Amount (₹)")

plt.tight_layout()

# plt.savefig(
#     CHART_DIR/"06_SIP_Boxplot_Age.png",
#     dpi=300
# )

gender = transactions["gender"].value_counts()

plt.figure(figsize=(7,7))

plt.pie(
    gender,
    labels=gender.index,
    autopct="%1.1f%%",
    startangle=90,
    explode=[0.03]*len(gender)
)

plt.title(
    "Investor Gender Distribution",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

# plt.savefig(
#     CHART_DIR/"07_Gender_Split.png",
#     dpi=300
# )

state_data = (
    sip_transactions
    .groupby("state")["amount_inr"]
    .sum()
    .sort_values()
)

plt.figure(figsize=(12,8))

state_data.plot(
    kind="barh",
    color="steelblue"
)

plt.title(
    "Total SIP Amount by State",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Total SIP Amount (₹)")

plt.ylabel("State")

plt.tight_layout()

# plt.savefig(
#     CHART_DIR/"08_State_SIP.png",
#     dpi=300
# )

tier = transactions["city_tier"].value_counts()

plt.figure(figsize=(7,7))

plt.pie(
    tier,
    labels=tier.index,
    autopct="%1.1f%%",
    startangle=90,
    explode=[0.05]*len(tier)
)

plt.title(
    "T30 vs B30 Investor Distribution",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

# plt.savefig(
#     CHART_DIR/"09_T30_B30.png",
#     dpi=300
# )

folio["month"] = pd.to_datetime(folio["month"])

fig = px.line(
    folio,
    x="month",
    y="total_folios_crore",
    markers=True,
    title="Mutual Fund Folio Growth (2022–2025)"
)

fig.add_annotation(
    x=str(folio["month"].iloc[0].date()),
    y=13.26,
    text="13.26 Cr",
    showarrow=True
)

fig.add_annotation(
    x=str(folio["month"].iloc[-1].date()),
    y=26.12,
    text="26.12 Cr",
    showarrow=True
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_title="Month",
    yaxis_title="Total Folios (Crore)"
)

# fig.write_image(
#     CHART_DIR/"10_Folio_Growth.png",
#     engine="kaleido"
# )

nav["date"] = pd.to_datetime(nav["date"])

top10 = (
    nav["amfi_code"]
    .drop_duplicates()
    .head(10)
)

nav_top = nav[nav["amfi_code"].isin(top10)]

pivot = nav_top.pivot_table(
    index="date",
    columns="amfi_code",
    values="nav"
)

returns = pivot.pct_change()

corr = returns.corr()

plt.figure(figsize=(12,10))

sns.heatmap(
    corr,
    cmap="coolwarm",
    annot=True,
    fmt=".2f",
    linewidths=0.5
)

plt.title(
    "Correlation Matrix of Daily NAV Returns",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

# plt.savefig(
#     CHART_DIR/"11_NAV_Correlation.png",
#     dpi=300
# )

sector = (
    portfolio
    .groupby("sector")["weight_pct"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9,9))

plt.pie(
    sector,
    labels=sector.index,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops=dict(width=0.4)
)

plt.title(
    "Sector Allocation Across Equity Funds",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

# plt.savefig(
#     CHART_DIR/"12_Sector_Allocation.png",
#     dpi=300
# )

fund_count = (
    fund["fund_house"]
    .value_counts()
    .head(15)
)

plt.figure(figsize=(12,6))

sns.barplot(
    x=fund_count.index,
    y=fund_count.values,
    hue=fund_count.index,
    palette="viridis",
    legend=False
)

plt.xticks(rotation=60)

plt.xlabel("Fund House")

plt.ylabel("Number of Schemes")

plt.title(
    "Top Fund Houses by Number of Schemes",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

# plt.savefig(
#     CHART_DIR/"13_Fund_Houses.png",
#     dpi=300
# )

count = transactions["transaction_type"].value_counts()

plt.figure(figsize=(8,6))

sns.barplot(
    x=count.index,
    y=count.values,
    hue=count.index,
    palette="Set2",
    legend=False
)

plt.xlabel("Transaction Type")

plt.ylabel("Count")

plt.title(
    "Distribution of Transaction Types",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

# plt.savefig(
#     CHART_DIR/"14_Transaction_Type.png",
#     dpi=300
# )

payment = (
    transactions["payment_mode"]
    .value_counts()
)

plt.figure(figsize=(10,6))

sns.barplot(
    x=payment.index,
    y=payment.values,
    hue=payment.index,
    palette="tab10",
    legend=False
)

plt.xticks(rotation=45)

plt.xlabel("Payment Mode")

plt.ylabel("Transactions")

plt.title(
    "Payment Mode Distribution",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

# plt.savefig(
#     CHART_DIR/"15_Payment_Mode.png",
#     dpi=300
# )

kyc = transactions["kyc_status"].value_counts()

plt.figure(figsize=(8,6))

sns.barplot(
    x=kyc.index,
    y=kyc.values,
    hue=kyc.index,
    palette="viridis",
    legend=False
)

plt.title("KYC Status Distribution")
plt.xlabel("KYC Status")
plt.ylabel("Number of Investors")

plt.tight_layout()

# plt.savefig(CHART_DIR/"16_KYC_Status.png", dpi=300)

transactions["annual_income_lakh"] = pd.to_numeric(
    transactions["annual_income_lakh"],
    errors="coerce"
)

income = transactions["annual_income_lakh"].dropna()

plt.figure(figsize=(10,6))

sns.histplot(
    data=income,
    bins=20,
    kde=True,
    color="steelblue"
)

plt.title(
    "Annual Income Distribution of Investors",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Annual Income (₹ Lakh)")

plt.ylabel("Number of Investors")

plt.grid(alpha=0.3)

plt.tight_layout()

# plt.savefig(
#     CHART_DIR/"17_Income_Distribution.png",
#     dpi=300
# )

scheme_count = (
    aum.groupby("fund_house")["num_schemes"]
    .max()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12,6))

sns.barplot(
    x=scheme_count.index,
    y=scheme_count.values,
    hue=scheme_count.index,
    palette="magma",
    legend=False
)

plt.xticks(rotation=60)

plt.title("Number of Schemes by Fund House")

plt.tight_layout()

# plt.savefig(CHART_DIR/"18_Number_of_Schemes.png", dpi=300)

top10 = (
    portfolio.sort_values("weight_pct", ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))

sns.barplot(
    data=top10,
    x="stock_name",
    y="weight_pct",
    hue="stock_name",
    palette="coolwarm",
    legend=False
)

plt.xticks(rotation=60)

plt.title("Top 10 Portfolio Holdings")

plt.ylabel("Weight (%)")

plt.tight_layout()

# plt.savefig(CHART_DIR/"19_Top_Stocks.png", dpi=300)

benchmark["date"] = pd.to_datetime(benchmark["date"])

fig = px.line(
    benchmark,
    x="date",
    y="close_value",
    color="index_name",
    title="Benchmark Index Performance (2022–2025)",
    markers=True
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    xaxis_title="Date",
    yaxis_title="Closing Value"
)

# fig.write_image(
#     CHART_DIR / "20_Benchmark_Performance.png"
# )

