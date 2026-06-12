-- 03_bank_adoption_rate.sql
-- Bank ecosystem expansion year-by-year
-- Shows the network effect: more banks = more transactions

SELECT
    year,
    MIN(banks_live_on_upi)                                 AS banks_at_year_start,
    MAX(banks_live_on_upi)                                 AS banks_at_year_end,
    MAX(banks_live_on_upi) - MIN(banks_live_on_upi)        AS banks_added_in_year,
    ROUND(
        100.0 * (MAX(banks_live_on_upi) - MIN(banks_live_on_upi))
        / NULLIF(MIN(banks_live_on_upi), 0),
    2)                                                     AS bank_growth_pct
FROM upi_monthly
WHERE banks_live_on_upi IS NOT NULL
GROUP BY year
ORDER BY year;