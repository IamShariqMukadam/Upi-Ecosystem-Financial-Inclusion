-- 06_financial_inclusion_gap.sql
-- Identifies digitally underserved states using Jan Dhan deposit-per-account
-- as a proxy for digital payment adoption.
--
-- LOGIC: Low deposit per account = financially included but cash-dependent
-- GAP   = (national avg - state avg) × accounts = untapped potential (₹ Crore)
--
-- FINDINGS:
--   12 states below national avg of ₹3,702/account
--   255.9M accounts in these states (55.8% of all Jan Dhan)
--   Total untapped potential: ₹12,417 Crore

WITH national_avg AS (
    SELECT
        SUM(number_of_pmjdy_accounts)                              AS total_accounts,
        SUM(deposit_in_rs__crore)                                  AS total_deposit_crore,
        (SUM(deposit_in_rs__crore) * 10000000.0)
        / SUM(number_of_pmjdy_accounts)                            AS avg_deposit_per_account_rs
    FROM jan_dhan_statewise
),
state_metrics AS (
    SELECT
        j.state_ut,
        j.number_of_pmjdy_accounts                                 AS accounts,
        j.deposit_in_rs__crore                                     AS deposit_crore,
        ROUND(
            (j.deposit_in_rs__crore * 10000000.0
            / j.number_of_pmjdy_accounts)::NUMERIC, 0)             AS deposit_per_account_rs,
        ROUND(n.avg_deposit_per_account_rs::NUMERIC, 0)            AS national_avg_rs,
        ROUND(
            ((n.avg_deposit_per_account_rs
            - (j.deposit_in_rs__crore * 10000000.0 / j.number_of_pmjdy_accounts))
            * j.number_of_pmjdy_accounts / 10000000.0)::NUMERIC, 2) AS gap_crore,
        ROUND(
            (j.deposit_in_rs__crore * 10000000.0 / j.number_of_pmjdy_accounts)
            / n.avg_deposit_per_account_rs * 100::NUMERIC, 1)       AS pct_of_national_avg,
        ROUND(
            j.number_of_pmjdy_accounts * 100.0
            / n.total_accounts::NUMERIC, 2)                         AS account_share_pct
    FROM jan_dhan_statewise j
    CROSS JOIN national_avg n
)
SELECT
    state_ut,
    accounts,
    deposit_crore,
    deposit_per_account_rs,
    national_avg_rs,
    gap_crore,
    pct_of_national_avg,
    account_share_pct,
    CASE
        WHEN gap_crore > 0 THEN 'Digitally Underserved'
        ELSE 'Above National Average'
    END                                                             AS inclusion_status,
    CASE
        WHEN gap_crore > 2000  THEN 'Critical Gap'
        WHEN gap_crore > 500   THEN 'High Gap'
        WHEN gap_crore > 0     THEN 'Moderate Gap'
        ELSE 'No Gap'
    END                                                             AS gap_severity
FROM state_metrics
ORDER BY gap_crore DESC;