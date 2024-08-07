WITH total_sales_per_store_type AS (
    SELECT
        dsd.store_type,
        SUM(dp.product_price * ot.product_quantity) AS total_sales
    FROM
        orders_table ot
    JOIN
        dim_products dp ON ot.product_code = dp.product_code
    JOIN
        dim_store_details dsd ON ot.store_code = dsd.store_code
    GROUP BY
        dsd.store_type
),
overall_total_sales AS (
    SELECT
        SUM(total_sales) AS total_sales
    FROM
        total_sales_per_store_type
)
SELECT
    ts.store_type,
    ts.total_sales,
    ROUND((ts.total_sales / ot.total_sales) * 100, 2) AS percentage_total
FROM
    total_sales_per_store_type ts
CROSS JOIN
    overall_total_sales ot;
