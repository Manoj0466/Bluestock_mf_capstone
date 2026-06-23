Bluestock Mutual Fund Analytics Platform
Data Dictionary

Dataset 1: 01_fund_master.csv

| Column Name        | Data Type | Description              |
| ------------------ | --------- | ------------------------ |
| amfi_code          | TEXT      | Unique AMFI scheme code  |
| fund_house         | TEXT      | Mutual fund company name |
| scheme_name        | TEXT      | Scheme name              |
| category           | TEXT      | Fund category            |
| sub_category       | TEXT      | Sub-category of fund     |
| plan               | TEXT      | Direct or Regular plan   |
| launch_date        | DATE      | Fund launch date         |
| benchmark          | TEXT      | Benchmark index          |
| expense_ratio_pct  | REAL      | Expense ratio percentage |
| exit_load_pct      | REAL      | Exit load percentage     |
| fund_manager       | TEXT      | Fund manager             |
| risk_category      | TEXT      | Risk classification      |
| sebi_category_code | TEXT      | SEBI category code       |

---

Dataset 2: 02_nav_history.csv


| Column Name      | Data Type | Description                       |
| ---------------- | --------- | --------------------------------- |
| amfi_code        | TEXT      | AMFI scheme code                  |
| date             | DATE      | NAV date                          |
| nav              | REAL      | Net Asset Value                   |
| daily_return_pct | REAL      | Daily percentage return (derived) |

---

 ataset 3: 03_aum_by_fund_house.csv


| Column Name      | Data Type | Description                       |
| ---------------- | --------- | --------------------------------- |
| fund_house       | TEXT      | Asset management company          |
| date             | DATE      | Quarter date                      |
| aum_crore        | REAL      | Assets Under Management (₹ Crore) |
| num_schemes      | INTEGER   | Number of schemes managed         |
| market_share_pct | REAL      | AMC market share percentage       |

---

Dataset 4: 04_monthly_sip_inflows.csv


| Column Name               | Data Type | Description                      |
| ------------------------- | --------- | -------------------------------- |
| month                     | DATE      | Month                            |
| sip_inflow_crore          | REAL      | SIP inflow amount                |
| active_sip_accounts_crore | REAL      | Active SIP accounts              |
| new_sip_accounts_lakh     | REAL      | New SIP registrations            |
| sip_aum_lakh_crore        | REAL      | SIP AUM                          |
| yoy_growth_pct            | REAL      | Year-over-year growth percentage |

---

Dataset 5: 05_category_inflows.csv


| Column Name      | Data Type | Description       |
| ---------------- | --------- | ----------------- |
| month            | DATE      | Month             |
| category         | TEXT      | Fund category     |
| net_inflow_crore | REAL      | Net inflow amount |

---

Dataset 6: 06_industry_folio_count.csv


| Column Name        | Data Type | Description   |
| ------------------ | --------- | ------------- |
| month              | DATE      | Month         |
| equity_folio_crore | REAL      | Equity folios |
| debt_folio_crore   | REAL      | Debt folios   |
| hybrid_folio_crore | REAL      | Hybrid folios |
| total_folio_crore  | REAL      | Total folios  |

---

Dataset 7: 07_scheme_performance.csv


| Column Name        | Data Type | Description                   |
| ------------------ | --------- | ----------------------------- |
| amfi_code          | TEXT      | Scheme code                   |
| return_1yr_pct     | REAL      | 1-year return                 |
| return_3yr_pct     | REAL      | 3-year CAGR                   |
| return_5yr_pct     | REAL      | 5-year CAGR                   |
| benchmark_3yr_pct  | REAL      | Benchmark return              |
| alpha              | REAL      | Excess return over benchmark  |
| beta               | REAL      | Market sensitivity            |
| sharpe_ratio       | REAL      | Risk-adjusted return          |
| sortino_ratio      | REAL      | Downside-risk-adjusted return |
| std_dev_ann_pct    | REAL      | Annualized volatility         |
| max_drawdown_pct   | REAL      | Maximum drawdown              |
| morningstar_rating | INTEGER   | Rating from 1–5               |

---

Dataset 8: 08_investor_transactions.csv


| Column Name        | Data Type | Description              |
| ------------------ | --------- | ------------------------ |
| investor_id        | TEXT      | Unique investor ID       |
| transaction_date   | DATE      | Transaction date         |
| amfi_code          | TEXT      | Fund code                |
| transaction_type   | TEXT      | SIP, Lumpsum, Redemption |
| amount_inr         | REAL      | Transaction amount       |
| state              | TEXT      | Investor state           |
| city               | TEXT      | Investor city            |
| city_tier          | TEXT      | T30/B30 classification   |
| age_group          | TEXT      | Investor age group       |
| gender             | TEXT      | Investor gender          |
| annual_income_lakh | REAL      | Annual income            |
| payment_mode       | TEXT      | Payment method           |
| kyc_status         | TEXT      | KYC verification status  |

---

Dataset 9: 09_portfolio_holdings.csv


| Column Name    | Data Type | Description           |
| -------------- | --------- | --------------------- |
| amfi_code      | TEXT      | Scheme code           |
| stock_symbol   | TEXT      | Stock ticker          |
| stock_name     | TEXT      | Company name          |
| sector         | TEXT      | Sector classification |
| weight_pct     | REAL      | Portfolio weight      |
| portfolio_date | DATE      | Portfolio date        |

---

Dataset 10: 10_benchmark_indices.csv


| Column Name    | Data Type | Description   |
| -------------- | --------- | ------------- |
| date           | DATE      | Trading date  |
| benchmark_name | TEXT      | Index name    |
| close_value    | REAL      | Closing value |

---

Data Quality Summary

| Dataset                  | Null Values     | Duplicate Rows | Status |
| ------------------------ | --------------- | -------------- | ------ |
| 01_fund_master           | 0               | 0              | Clean  |
| 02_nav_history           | 0               | 0              | Clean  |
| 03_aum_by_fund_house     | 0               | 0              | Clean  |
| 04_monthly_sip_inflows   | 12 (YoY Growth) | 0              | Clean  |
| 05_category_inflows      | 0               | 0              | Clean  |
| 06_industry_folio_count  | 0               | 0              | Clean  |
| 07_scheme_performance    | 0               | 0              | Clean  |
| 08_investor_transactions | 0               | 0              | Clean  |
| 09_portfolio_holdings    | 0               | 0              | Clean  |
| 10_benchmark_indices     | 0               | 0              | Clean  |

