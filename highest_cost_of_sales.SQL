WITH sales_per_month AS (
    SELECT
        EXTRACT(YEAR FROM dcd.date_payment_confirmed) AS year,
        EXTRACT(MONTH FROM dcd.date_payment_confirmed) AS month,
        SUM(dp.product_price * ot.product_quantity) AS total_sales
    FROM
        orders_table ot
    JOIN
        dim_products dp ON ot.product_code = dp.product_code
    JOIN
        dim_card_details dcd ON ot.card_number = dcd.card_number
    GROUP BY
        EXTRACT(YEAR FROM dcd.date_payment_confirmed),
        EXTRACT(MONTH FROM dcd.date_payment_confirmed)
)
SELECT
    total_sales,
    year,
    month
FROM
    sales_per_month
ORDER BY
    total_sales DESC
LIMIT 10;

