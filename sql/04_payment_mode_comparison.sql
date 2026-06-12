-- 04_payment_mode_comparison.sql
-- Which AePS payment type is dominant in 2024?
-- Table: npci_products (AePS BHIM Aadhaar Pay, Cash Withdrawal, Funds Transfer)
-- NOTE: Covers AePS products only (2024). Full UPI vs IMPS vs NEFT comparison
--       requires the Kaggle NPCI Products Statistics dataset (see README).

SELECT
    product_name,
    year,
    COUNT(*)                                               AS months,
    ROUND(SUM(volume_mn)::NUMERIC, 2)                      AS total_volume_mn,
    ROUND(AVG(volume_mn)::NUMERIC, 2)                      AS avg_monthly_volume_mn,
    ROUND(MAX(volume_mn)::NUMERIC, 2)                      AS peak_monthly_volume_mn,
    RANK() OVER (
        PARTITION BY year
        ORDER BY SUM(volume_mn) DESC
    )                                                      AS rank_by_volume
FROM npci_products
GROUP BY product_name, year
ORDER BY year, rank_by_volume;