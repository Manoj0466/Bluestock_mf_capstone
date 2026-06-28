import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import warnings
warnings.filterwarnings("ignore")

nav = pd.read_csv("Processed data/clean_nav_history.csv")
benchmark = pd.read_csv("Processed data/clean_benchmark_indices.csv")
fund = pd.read_csv("Processed data/clean_fund_master.csv")

# print("\nNAV Shape :", nav.shape)
# print("Benchmark Shape :", benchmark.shape)
# print("Fund Master Shape :", fund.shape)

nav["date"] = pd.to_datetime(nav["date"])

benchmark["date"] = pd.to_datetime(benchmark["date"])

nav = nav.sort_values(["amfi_code", "date"])

benchmark = benchmark.sort_values(["index_name", "date"])

nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
    .pct_change()
)

nav["daily_return"] = nav["daily_return"].fillna(0)

# print("Daily Returns Calculated Successfully.")

nav.to_csv(
    "Processed data/daily_returns.csv",
    index=False
)

returns = nav["daily_return"]

# print("\nReturn Distribution Statistics")
# print("-"*40)

# print("Mean      :", returns.mean())
# print("Median    :", returns.median())
# print("Std Dev   :", returns.std())
# print("Minimum   :", returns.min())
# print("Maximum   :", returns.max())
# print("Skewness  :", returns.skew())
# print("Kurtosis  :", returns.kurt())

plt.figure(figsize=(10,6))

plt.hist(
    returns,
    bins=60,
    edgecolor="black"
)

plt.title("Daily Return Distribution")
plt.xlabel("Daily Return")
plt.ylabel("Frequency")

plt.grid(True)

plt.tight_layout()

# plt.savefig(
#     "Charts/21_Return_Distribution.png",
#     dpi=300
# )

plt.close()


# Create Empty List

cagr_result = []

# Years Required

years_required = {
    "1Y":1,
    "3Y":3,
    "5Y":5
}

# Today's Date

latest_date = nav["date"].max()

# Loop Every Fund

for code in nav["amfi_code"].unique():

    temp = nav[
        nav["amfi_code"] == code
    ].sort_values("date")

    row = {}

    row["amfi_code"] = code

    # Scheme Name

    try:

        row["scheme_name"] = fund.loc[
            fund["amfi_code"] == code,
            "scheme_name"
        ].values[0]

    except:

        row["scheme_name"] = "Unknown"

    end_nav = temp.iloc[-1]["nav"]

    end_date = temp.iloc[-1]["date"]

    # Calculate for 1Y 3Y 5Y

    for label, yr in years_required.items():

        start_date = end_date - pd.DateOffset(years=yr)

        hist = temp[
            temp["date"] <= start_date
        ]

        if len(hist)==0:

            row[label] = np.nan

            continue

        start_nav = hist.iloc[-1]["nav"]

        cagr = (
            (end_nav/start_nav)**(1/yr)
        )-1

        row[label] = round(cagr*100,2)

    cagr_result.append(row)

# Convert DataFrame

cagr_df = pd.DataFrame(cagr_result)

# Save CSV

# cagr_df.to_csv(
#     "Processed data/cagr_table.csv",
#     index=False
# )

# print("\nTop Funds based on 3 Year CAGR")

# print(
#     cagr_df.sort_values(
#         "3Y",
#         ascending=False
#     ).head(10)
# )

RISK_FREE_RATE = 0.065    # 6.5%
TRADING_DAYS = 252

sharpe_list = []

for code in nav["amfi_code"].unique():

    fund_returns = nav.loc[
        nav["amfi_code"] == code,
        "daily_return"
    ]

    fund_returns = fund_returns.dropna()

    if len(fund_returns) < 2:
        continue

    annual_return = fund_returns.mean() * TRADING_DAYS

    annual_std = fund_returns.std() * np.sqrt(TRADING_DAYS)

    if annual_std == 0:
        sharpe = np.nan
    else:
        sharpe = (annual_return - RISK_FREE_RATE) / annual_std

    try:
        scheme = fund.loc[
            fund["amfi_code"] == code,
            "scheme_name"
        ].values[0]
    except:
        scheme = "Unknown"

    sharpe_list.append([
        code,
        scheme,
        round(annual_return * 100, 2),
        round(annual_std * 100, 2),
        round(sharpe, 4)
    ])

sharpe_df = pd.DataFrame(
    sharpe_list,
    columns=[
        "amfi_code",
        "scheme_name",
        "annual_return(%)",
        "annual_volatility(%)",
        "sharpe_ratio"
    ]
)

sharpe_df["Rank"] = (
    sharpe_df["sharpe_ratio"]
    .rank(ascending=False)
    .astype(int)
)

sharpe_df = sharpe_df.sort_values("Rank")

# print("\nTop 10 Funds by Sharpe Ratio\n")

# print(
#     sharpe_df[
#         [
#             "scheme_name",
#             "sharpe_ratio",
#             "Rank"
#         ]
#     ].head(10)
# )

# sharpe_df.to_csv(
#     "Processed data/sharpe_ratio.csv",
#     index=False
# )

sortino_list = []

for code in nav["amfi_code"].unique():

    fund_returns = nav.loc[
        nav["amfi_code"] == code,
        "daily_return"
    ]

    fund_returns = fund_returns.dropna()

    if len(fund_returns) < 2:
        continue

    annual_return = fund_returns.mean() * TRADING_DAYS

    downside_returns = fund_returns[
        fund_returns < 0
    ]

    if len(downside_returns) == 0:

        downside_std = np.nan

    else:

        downside_std = (
            downside_returns.std()
            * np.sqrt(TRADING_DAYS)
        )

    if (
        pd.isna(downside_std)
        or downside_std == 0
    ):

        sortino = np.nan

    else:

        sortino = (
            annual_return - RISK_FREE_RATE
        ) / downside_std

    try:

        scheme = fund.loc[
            fund["amfi_code"] == code,
            "scheme_name"
        ].values[0]

    except:

        scheme = "Unknown"

    sortino_list.append([
        code,
        scheme,
        round(sortino, 4)
    ])

sortino_df = pd.DataFrame(
    sortino_list,
    columns=[
        "amfi_code",
        "scheme_name",
        "sortino_ratio"
    ]
)

sortino_df["Rank"] = (
    sortino_df["sortino_ratio"]
    .rank(ascending=False)
    .astype(int)
)

sortino_df = sortino_df.sort_values("Rank")

# print("\nTop 10 Funds by Sortino Ratio\n")

# print(
#     sortino_df[
#         [
#             "scheme_name",
#             "sortino_ratio",
#             "Rank"
#         ]
#     ].head(10)
# )

# sortino_df.to_csv(
#     "Processed data/sortino_ratio.csv",
#     index=False
# )


# Select NIFTY 100 Benchmark
benchmark_data = benchmark[
    benchmark["index_name"].str.upper() == "NIFTY100"
].copy()

benchmark_data = benchmark_data.sort_values("date")

# Calculate Benchmark Daily Returns
benchmark_data["benchmark_return"] = benchmark_data["close_value"].pct_change()

benchmark_data = benchmark_data.dropna()

alpha_beta_list = []

for code in nav["amfi_code"].unique():

    fund_data = nav[
        nav["amfi_code"] == code
    ][["date", "daily_return"]]

    merged = pd.merge(
        fund_data,
        benchmark_data[["date", "benchmark_return"]],
        on="date",
        how="inner"
    )

    merged = merged.dropna()

    if len(merged) < 30:
        continue

    regression = linregress(
        merged["benchmark_return"],
        merged["daily_return"]
    )
    # print(regression)

    beta = regression.slope

    alpha = regression.intercept * 252

    try:
        scheme = fund.loc[
            fund["amfi_code"] == code,
            "scheme_name"
        ].values[0]
    except:
        scheme = "Unknown"
    
    # print("Appending:", code)
    alpha_beta_list.append([
        code,
        scheme,
        round(alpha,6),
        round(beta,4),
        round(regression.rvalue**2,4)
    ])
    # print(len(alpha_beta_list))

alpha_beta_df = pd.DataFrame(
    alpha_beta_list,
    columns=[
        "amfi_code",
        "scheme_name",
        "alpha",
        "beta",
        "R_squared"
    ]
)

alpha_beta_df["Alpha Rank"] = (
    alpha_beta_df["alpha"]
    .rank(ascending=False)
    .astype(int)
)

alpha_beta_df = alpha_beta_df.sort_values(
    "Alpha Rank"
)

# print("\nTop 10 Funds by Alpha\n")

# print(
#     alpha_beta_df[
#         [
#             "scheme_name",
#             "alpha",
#             "beta",
#             "Alpha Rank"
#         ]
#     ].head(10)
# )

# alpha_beta_df.to_csv(
#     "Processed data/alpha_beta.csv",
#     index=False
# )

# print(alpha_beta_df.head())
# print(alpha_beta_df.shape)

drawdown_list = []

for code in nav["amfi_code"].unique():

    temp = nav[
        nav["amfi_code"] == code
    ].copy()

    temp = temp.sort_values("date")

    temp["Running_Max"] = temp["nav"].cummax()

    temp["Drawdown"] = (
        temp["nav"] /
        temp["Running_Max"]
    ) - 1

    worst_row = temp.loc[
        temp["Drawdown"].idxmin()
    ]

    end_date = worst_row["date"]

    start_data = temp[
        temp["date"] <= end_date
    ]

    start_date = start_data.loc[
        start_data["nav"].idxmax(),
        "date"
    ]

    try:
        scheme = fund.loc[
            fund["amfi_code"] == code,
            "scheme_name"
        ].values[0]
    except:
        scheme = "Unknown"

    drawdown_list.append([
        code,
        scheme,
        round(worst_row["Drawdown"]*100,2),
        start_date.date(),
        end_date.date()
    ])

drawdown_df = pd.DataFrame(
    drawdown_list,
    columns=[
        "amfi_code",
        "scheme_name",
        "Maximum_Drawdown(%)",
        "Drawdown_Start",
        "Drawdown_End"
    ]
)

drawdown_df["Rank"] = (
    drawdown_df["Maximum_Drawdown(%)"]
    .rank(ascending=False)
    .astype(int)
)

drawdown_df = drawdown_df.sort_values(
    "Maximum_Drawdown(%)",
    ascending=False
)

# print("\nTop 10 Funds with Lowest Drawdown\n")

# print(
#     drawdown_df[
#         [
#             "scheme_name",
#             "Maximum_Drawdown(%)"
#         ]
#     ].head(10)
# )

# drawdown_df.to_csv(
#     "Processed data/drawdown.csv",
#     index=False
# )

# Expense Ratio
expense = fund[["amfi_code", "expense_ratio_pct"]].copy()

# Merge all rankings
scorecard = cagr_df[["amfi_code", "scheme_name", "3Y"]].copy()

scorecard = scorecard.merge(
    sharpe_df[["amfi_code", "sharpe_ratio"]],
    on="amfi_code",
    how="left"
)

scorecard = scorecard.merge(
    alpha_beta_df[["amfi_code", "alpha"]],
    on="amfi_code",
    how="left"
)

scorecard = scorecard.merge(
    drawdown_df[["amfi_code", "Maximum_Drawdown(%)"]],
    on="amfi_code",
    how="left"
)

scorecard = scorecard.merge(
    expense,
    on="amfi_code",
    how="left"
)

# Ranking

scorecard["Return Rank"] = scorecard["3Y"].rank(ascending=False)

scorecard["Sharpe Rank"] = scorecard["sharpe_ratio"].rank(ascending=False)

scorecard["Alpha Rank"] = scorecard["alpha"].rank(ascending=False)

scorecard["Expense Rank"] = scorecard["expense_ratio_pct"].rank(ascending=True)

scorecard["Drawdown Rank"] = scorecard["Maximum_Drawdown(%)"].rank(ascending=False)

# Composite Score

scorecard["Score"] = (

      scorecard["Return Rank"] * 0.30

    + scorecard["Sharpe Rank"] * 0.25

    + scorecard["Alpha Rank"] * 0.20

    + scorecard["Expense Rank"] * 0.15

    + scorecard["Drawdown Rank"] * 0.10

)

# Convert to 0-100

max_score = scorecard["Score"].max()

min_score = scorecard["Score"].min()

scorecard["Fund Score"] = (

    (max_score - scorecard["Score"])

    /(max_score-min_score)

)*100

scorecard["Fund Score"] = scorecard["Fund Score"].round(2)

scorecard = scorecard.sort_values(
    "Fund Score",
    ascending=False
)

# scorecard.to_csv(
#     "Processed data/fund_scorecard.csv",
#     index=False
# )

# print("\nTop 10 Funds")

# print(scorecard[[
# "scheme_name",
# "Fund Score"
# ]
# ].head(10)
# )

# Top 5 Funds

top5 = scorecard.head(5)["amfi_code"].tolist()

# Last 3 Years

latest = nav["date"].max()

start = latest - pd.DateOffset(years=3)

plt.figure(figsize=(14,7))

# Plot Top Funds

for code in top5:

    temp = nav[

        (nav["amfi_code"]==code)

        &

        (nav["date"]>=start)

    ].copy()

    temp["Growth"]=(temp["nav"]/temp.iloc[0]["nav"])*100

    name = fund.loc[
        fund["amfi_code"]==code,
        "scheme_name"
    ].values[0]

    plt.plot(
        temp["date"],
        temp["Growth"],
        label=name
    )

# Plot NIFTY50

n50 = benchmark[
    benchmark["index_name"]=="NIFTY50"
].copy()

n50 = n50[
    n50["date"]>=start
]

n50["Growth"]=(

n50["close_value"]

/

n50.iloc[0]["close_value"]

)*100

plt.plot(

n50["date"],

n50["Growth"],

linewidth=3,

label="NIFTY50"

)

# Plot NIFTY100

n100 = benchmark[
    benchmark["index_name"]=="NIFTY100"
].copy()

n100 = n100[
    n100["date"]>=start
]

n100["Growth"]=(

n100["close_value"]

/

n100.iloc[0]["close_value"]

)*100

plt.plot(

n100["date"],

n100["Growth"],

linewidth=3,

label="NIFTY100"

)

plt.title("Top 5 Funds vs Benchmarks (3 Years)")

plt.xlabel("Date")

plt.ylabel("Growth Index")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(

"Charts/22_Benchmark_Comparison.png",

dpi=300

)

plt.close()

print("Benchmark Comparison Chart Saved.")


tracking = []

# Benchmark Daily Returns

bench = benchmark[
benchmark["index_name"]=="NIFTY100"
].copy()

bench = bench.sort_values("date")

bench["benchmark_return"] = bench["close_value"].pct_change()

for code in top5:

    temp = nav[
        nav["amfi_code"]==code
    ][["date","daily_return"]]

    merge = pd.merge(

        temp,

        bench[["date","benchmark_return"]],

        on="date",

        how="inner"

    )

    tracking_error = (

        (merge["daily_return"]

        -

        merge["benchmark_return"]).std()

        *

        np.sqrt(252)

    )

    name = fund.loc[
        fund["amfi_code"]==code,
        "scheme_name"
    ].values[0]

    tracking.append([

        code,

        name,

        round(tracking_error,6)

    ])

tracking_df = pd.DataFrame(

tracking,

columns=[

"amfi_code",

"scheme_name",

"Tracking Error"

]

)

tracking_df.to_csv(

"Processed data/tracking_error.csv",

index=False

)


