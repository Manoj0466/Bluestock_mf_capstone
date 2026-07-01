import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")



nav = pd.read_csv("Processed data/clean_nav_history.csv")

fund = pd.read_csv("Processed data/clean_fund_master.csv")

transactions = pd.read_csv("Processed data/clean_investor_transactions.csv")

portfolio = pd.read_csv( "Processed data/clean_portfolio_holdings.csv")

performance = pd.read_csv("Processed data/clean_scheme_performance.csv")

benchmark = pd.read_csv("Processed data/clean_benchmark_indices.csv")

nav["date"] = pd.to_datetime(nav["date"])

transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])

benchmark["date"] = pd.to_datetime(benchmark["date"])

nav = nav.sort_values(
    ["amfi_code", "date"]
)

nav["daily_return"] = (nav.groupby("amfi_code")["nav"].pct_change())

nav["daily_return"] = nav["daily_return"].fillna(0)

# print("Daily Returns Calculated Successfully.")

var_list = []

for code in nav["amfi_code"].unique():

    returns = nav.loc[
        nav["amfi_code"] == code,
        "daily_return"
    ].dropna()

    if len(returns) == 0:
        continue

    var95 = np.percentile(returns, 5)

    cvar95 = returns[returns <= var95].mean()

    try:
        scheme = fund.loc[
            fund["amfi_code"] == code,
            "scheme_name"
        ].values[0]
    except:
        scheme = "Unknown"

    var_list.append([
        code,
        scheme,
        round(var95 * 100, 4),
        round(cvar95 * 100, 4)
    ])

var_df = pd.DataFrame(

    var_list,

    columns=[

        "amfi_code",

        "scheme_name",

        "VaR_95(%)",

        "CVaR_95(%)"

    ]

)

var_df = var_df.sort_values("VaR_95(%)")

# var_df.to_csv("Processed data/var_cvar_report.csv", index=False)

# print("\nTop 10 Lowest Risk Funds\n")

# print(var_df.head(10))


# Rolling 90-Day Sharpe Ratio

RISK_FREE_RATE = 0.065
TRADING_DAYS = 252
WINDOW = 90



selected_funds = fund["amfi_code"].head(5).tolist()

plt.figure(figsize=(14,7))

for code in selected_funds:

    temp = nav[
        nav["amfi_code"] == code
    ].copy()

    temp = temp.sort_values("date")

    returns = temp["daily_return"]

    rolling_mean = (
        returns.rolling(WINDOW).mean()
        * TRADING_DAYS
    )

    rolling_std = (
        returns.rolling(WINDOW).std()
        * np.sqrt(TRADING_DAYS)
    )

    rolling_sharpe = (
        (rolling_mean - RISK_FREE_RATE)
        / rolling_std
    )

    try:

        scheme = fund.loc[
            fund["amfi_code"] == code,
            "scheme_name"
        ].values[0]

    except:

        scheme = "Unknown"

    plt.plot(
        temp["date"],
        rolling_sharpe,
        label=scheme
    )

plt.title("Rolling 90-Day Sharpe Ratio")

plt.xlabel("Date")

plt.ylabel("Sharpe Ratio")

plt.grid(True)

plt.legend()

plt.tight_layout()

# plt.savefig(
#     "Charts/rolling_sharpe_chart.png",
#     dpi=300
# )

# plt.close()

# print("Rolling Sharpe Chart Saved Successfully.")

# Investor Cohort Analysis

first_txn = (
    transactions
    .groupby("investor_id")["transaction_date"]
    .min()
    .reset_index()
)

first_txn.rename(
    columns={"transaction_date": "first_transaction"},
    inplace=True
)



first_txn["cohort_year"] = pd.to_datetime(
    first_txn["first_transaction"]
).dt.year

transactions = transactions.merge(
    first_txn,
    on="investor_id",
    how="left"
)


sip = transactions[
    transactions["transaction_type"].str.upper() == "SIP"
].copy()


avg_sip = (
    sip.groupby("cohort_year")["amount_inr"]
    .mean()
    .reset_index()
)

avg_sip.rename(
    columns={"amount_inr": "average_sip_amount"},
    inplace=True
)

total_investment = (
    sip.groupby("cohort_year")["amount_inr"]
    .sum()
    .reset_index()
)

total_investment.rename(
    columns={"amount_inr": "total_investment"},
    inplace=True
)


investor_count = (
    first_txn.groupby("cohort_year")["investor_id"]
    .nunique()
    .reset_index()
)

investor_count.rename(
    columns={"investor_id": "number_of_investors"},
    inplace=True
)

fund_pref = (
    sip.groupby(["cohort_year", "amfi_code"])
    .size()
    .reset_index(name="count")
)

fund_pref = fund_pref.sort_values(
    ["cohort_year", "count"],
    ascending=[True, False]
)

fund_pref = (
    fund_pref
    .groupby("cohort_year")
    .first()
    .reset_index()
)


fund_pref = fund_pref.merge(
    fund[["amfi_code", "scheme_name"]],
    on="amfi_code",
    how="left"
)

fund_pref = fund_pref[
    ["cohort_year", "scheme_name"]
]

fund_pref.rename(
    columns={
        "scheme_name": "most_preferred_fund"
    },
    inplace=True
)

cohort = avg_sip.merge(
    total_investment,
    on="cohort_year"
)

cohort = cohort.merge(
    investor_count,
    on="cohort_year"
)

cohort = cohort.merge(
    fund_pref,
    on="cohort_year"
)

cohort["average_sip_amount"] = cohort["average_sip_amount"].round(2)
cohort["total_investment"] = cohort["total_investment"].round(2)

# cohort.to_csv(
#     "Processed data/cohort_analysis.csv",
#     index=False
# )

# print("\nCohort Analysis Completed.\n")
# print(cohort)

# SIP Continuation Analysis


sip = transactions[
    transactions["transaction_type"].str.upper() == "SIP"
].copy()



sip = sip.sort_values(
    ["investor_id", "transaction_date"]
)


sip["gap_days"] = (

    sip.groupby("investor_id")["transaction_date"]

    .diff()

    .dt.days

)


avg_gap = (

    sip.groupby("investor_id")["gap_days"]

    .mean()

    .reset_index()

)

avg_gap.rename(

    columns={

        "gap_days":"average_gap_days"

    },

    inplace=True

)


sip_count = (

    sip.groupby("investor_id")

    .size()

    .reset_index(name="sip_count")

)


continuity = avg_gap.merge(

    sip_count,

    on="investor_id"

)


continuity = continuity[
    continuity["sip_count"] >= 6
]


continuity["status"] = np.where(

    continuity["average_gap_days"] > 35,

    "At Risk",

    "Healthy"

)


continuity["average_gap_days"] = (

    continuity["average_gap_days"]

    .round(2)

)


# continuity.to_csv(

#     "Processed data/sip_continuity.csv",

#     index=False

# )

# print("\nSIP Continuation Analysis Completed.\n")

# print(continuity.head(10))


# Simple Fund Recommendation System


risk = input(
    "\nEnter Risk Appetite (Low / Moderate / High / Very High): "
).strip().title()


recommend = fund.merge(
    performance[["amfi_code", "sharpe_ratio"]],
    on="amfi_code",
    how="left"
)


recommend = recommend[

    recommend["risk_category"]

    .str.title()

    == risk

]


recommend = recommend.sort_values(

    "sharpe_ratio",

    ascending=False

)

top3 = recommend.head(3)


print("\nRecommended Funds\n")

print(

    top3[

        [

            "scheme_name",

            "fund_house",

            "category",

            "risk_category",

            "sharpe_ratio"

        ]

    ]

)


# top3.to_csv(

#     "Processed data/fund_recommendation.csv",

#     index=False

# )

# print("\nRecommendation Saved Successfully.")


# Sector Concentration Analysis (HHI)


portfolio["weight_decimal"] = portfolio["weight_pct"] / 100

portfolio["weight_square"] = (

    portfolio["weight_decimal"] ** 2

)


sector_hhi = (

    portfolio.groupby("amfi_code")["weight_square"]

    .sum()

    .reset_index()

)

sector_hhi.rename(

    columns={

        "weight_square":"HHI"

    },

    inplace=True

)


sector_hhi = sector_hhi.merge(

    fund[

        ["amfi_code","scheme_name"]

    ],

    on="amfi_code",

    how="left"

)


# sector_hhi = sector_hhi.sort_values(

#     "HHI",

#     ascending=False

# )

# sector_hhi.to_csv(

#     "Processed data/sector_hhi.csv",

#     index=False

# )

# print("\nSector HHI Saved Successfully.\n")

# print(sector_hhi.head(10))


# Sector HHI Chart


plt.figure(figsize=(14,7))

plt.bar(

    sector_hhi["scheme_name"],

    sector_hhi["HHI"]

)

plt.xticks(

    rotation=90

)

plt.xlabel("Fund")

plt.ylabel("HHI")

plt.title("Sector Concentration Risk (HHI)")

plt.grid(axis="y")

plt.tight_layout()

# plt.savefig(

#     "Charts/sector_hhi_chart.png",

#     dpi=300

# )

# plt.close()

# print("Sector HHI Chart Saved Successfully.")









