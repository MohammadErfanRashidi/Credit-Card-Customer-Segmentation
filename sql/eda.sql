-- Average balance by purchase activity level
SELECT
    CASE 
        WHEN purchases = 0 THEN 'No Purchases'
        WHEN purchases < 1000 THEN 'Low'
        WHEN purchases < 5000 THEN 'Medium'
        ELSE 'High'
    END AS purchases_group,
    COUNT(*) AS customers,
    ROUND(AVG(balance), 2) AS avg_balance,
    ROUND(AVG(cash_advance), 2) AS avg_cash_advance,
    ROUND(AVG(credit_limit), 2) AS avg_credit_limit
FROM credit_card
GROUP BY purchases_group
ORDER BY FIELD(purchases_group, 'No purchases', 'Low', 'Medium', 'High');

-- How many customers never made purchases and never took cash
SELECT
    SUM(CASE WHEN purchases = 0 THEN 1 ELSE 0 END) AS zero_purchase,
    SUM(CASE WHEN cash_advance = 0 THEN 1 ELSE 0 END) AS zero_cash_adv,
    SUM(CASE WHEN oneoff_purchases = 0 AND installments_purchases = 0 THEN 1 ELSE 0 END) AS no_purchase,
    ROUND(AVG(prc_full_payment), 2) AS avg_full_payment,
    SUM(CASE WHEN prc_full_payment = 0 THEN 1 ELSE 0 END) AS never_fully_pay
FROM credit_card;

-- Average balance and purchases by tenure 
SELECT 
    CASE 
        WHEN tenure <= 8 THEN '6-8 months'
        WHEN tenure <= 10 THEN '9-10 months'  
        ELSE '11-12 months' 
    END AS tenure_bin,
    COUNT(*) AS customers,
    ROUND(AVG(balance), 2) AS avg_balance,
    ROUND(AVG(purchases), 2) AS avg_purchase,
    ROUND(AVG(cash_advance), 2) AS avg_cash_adv,
    ROUND(AVG(credit_limit), 2) AS avg_credit_limit,
    ROUND(AVG(prc_full_payment), 2) AS avg_full_payment
FROM credit_card
GROUP BY tenure_bin
ORDER BY FIELD(tenure_bin, '6-8 months', '9-10 months', '11-12 months');

-- Purchase to credit limit
SELECT
    ROUND(AVG(purchases / NULLIF(credit_limit, 0)), 2) AS avg_util_purchases,
    ROUND(AVG((purchases + cash_advance) / NULLIF(credit_limit, 0)), 2) AS avg_util_total
FROM credit_card;

-- Count of distinct values per categorical features 
SELECT
    COUNT(DISTINCT tenure) AS dis_tenure,
    COUNT(DISTINCT cash_advance_trx) AS dis_cash_adv_trx,
    COUNT(DISTINCT purchases_trx) AS dis_purchases_trx,
    ROUND(AVG(purchases_trx), 2) AS avg_purch_trx,
    ROUND(AVG(cash_advance_trx), 2) AS avg_cash_trx
FROM credit_card;