SELECT scheme_name, expense_ratio_pct
FROM dim_fund
ORDER BY expense_ratio_pct DESC
LIMIT 5;

SELECT amfi_code,
AVG(nav) avg_nav
FROM fact_nav
GROUP BY amfi_code;

SELECT state,
COUNT(*) total_transactions
FROM fact_transactions
GROUP BY state;

SELECT SUM(amount_inr)
FROM fact_transactions;

SELECT category,
COUNT(*)
FROM dim_fund
GROUP BY category;

SELECT scheme_name
FROM dim_fund
WHERE expense_ratio_pct < 1;

SELECT AVG(sharpe_ratio)
FROM fact_performance;

SELECT amfi_code,
return_3yr_pct
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 10;

SELECT COUNT(*)
FROM fact_transactions
WHERE transaction_type='Sip';

SELECT SUM(amount_inr)
FROM fact_transactions
WHERE transaction_type='Redemption';