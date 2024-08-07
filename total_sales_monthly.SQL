-- Query to find out which months have produced the most sales
SELECT
    ddt.month,
    SUM(dp.product_price * ot.product_quantity) AS total_sales
FROM
    orders_table ot
JOIN
    dim_products dp ON ot.product_code = dp.product_code
JOIN
    dim_date_times ddt ON ot.date_uuid = ddt.date_uuid
GROUP BY
    ddt.month
ORDER BY
    total_sales DESC;
