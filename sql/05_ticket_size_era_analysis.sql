-- 05_ticket_size_era_analysis.sql
-- Tracks avg transaction size by era
-- Identifies the shift from high-value bank transfers to micro-payments

SELECT
    era,
    COUNT(*)                                               AS months,
    ROUND(AVG(volume_crore)::NUMERIC, 0)                   AS avg_monthly_volume_crore,
    ROUND(AVG(avg_ticket_size_rs)::NUMERIC, 0)             AS avg_ticket_rs,
    ROUND(MIN(avg_ticket_size_rs)::NUMERIC, 0)             AS min_ticket_rs,
    ROUND(MAX(avg_ticket_size_rs)::NUMERIC, 0)             AS max_ticket_rs,
    ROUND(AVG(volume_mom_pct)::NUMERIC, 2)                 AS avg_mom_growth_pct,
    MIN(date)::DATE                                        AS era_start,
    MAX(date)::DATE                                        AS era_end,
    CASE
        WHEN AVG(avg_ticket_size_rs) > 1500 THEN 'High-Value Transfer Dominant'
        WHEN AVG(avg_ticket_size_rs) BETWEEN 1000 AND 1500 THEN 'Transition / Mixed Use'
        WHEN AVG(avg_ticket_size_rs) < 1000  THEN 'Micro-Payment Era'
    END                                                    AS payment_regime
FROM upi_monthly
GROUP BY era
ORDER BY era_start;