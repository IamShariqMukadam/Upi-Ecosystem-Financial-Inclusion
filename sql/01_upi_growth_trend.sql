-- 01_yoy_performance.sql
-- Year-over-year UPI performance with growth rates
-- Table: upi_monthly | Column: volume_crore (crore transactions)

SELECT
    year,
    COUNT(*)                                              AS months_of_data,
    ROUND(SUM(volume_crore)::NUMERIC, 0)                  AS total_volume_crore,
    ROUND(SUM(value_crore)::NUMERIC, 0)                   AS total_value_crore,
    ROUND(AVG(avg_ticket_size_rs)::NUMERIC, 0)            AS avg_ticket_size_rs,
    ROUND(AVG(banks_live_on_upi)::NUMERIC, 0)             AS avg_banks_on_upi,
    ROUND(
        100.0 * (SUM(volume_crore) - LAG(SUM(volume_crore)) OVER (ORDER BY year))
        / NULLIF(LAG(SUM(volume_crore)) OVER (ORDER BY year), 0),
    2)                                                    AS yoy_volume_growth_pct
FROM upi_monthly
GROUP BY year
ORDER BY year;