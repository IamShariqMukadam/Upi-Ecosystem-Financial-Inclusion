-- 02_p2p_vs_p2m_shift.sql
-- The platform shift story: personal transfers → merchant payments
-- Table: upi_p2p_p2m | p2m_share_pct computed during cleaning

SELECT
    DATE_TRUNC('year', date)::DATE                         AS year,
    COUNT(*)                                               AS months,
    ROUND(AVG(p2m_share_pct)::NUMERIC, 2)                  AS avg_p2m_share_pct,
    ROUND(MIN(p2m_share_pct)::NUMERIC, 2)                  AS min_p2m_share_pct,
    ROUND(MAX(p2m_share_pct)::NUMERIC, 2)                  AS max_p2m_share_pct,
    ROUND(
        AVG(p2m_share_pct)
        - LAG(AVG(p2m_share_pct)) OVER (ORDER BY DATE_TRUNC('year', date)),
    2)                                                     AS p2m_share_yoy_change
FROM upi_p2p_p2m
GROUP BY DATE_TRUNC('year', date)
ORDER BY year;