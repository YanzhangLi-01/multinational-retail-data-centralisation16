WITH SalesWithTimestamps AS (
    SELECT
        o.product_code,
        o.product_quantity,
        p.product_price,
        (o.product_quantity * p.product_price) AS total_sales,
        -- Combine date and time into a full timestamp
        TO_TIMESTAMP(
            d.year || '-' || d.month || '-' || d.day || ' ' || d.timestamp,
            'YYYY-MM-DD HH24:MI:SS'
        ) AS sale_timestamp
    FROM
        orders_table o
    JOIN
        dim_products p ON o.product_code = p.product_code
    JOIN
        dim_date_times d ON o.date_uuid = d.date_uuid
),
TimeDifferences AS (
    SELECT
        EXTRACT(YEAR FROM sale_timestamp) AS year,
        EXTRACT(EPOCH FROM (
            LEAD(sale_timestamp) OVER (PARTITION BY EXTRACT(YEAR FROM sale_timestamp) ORDER BY sale_timestamp) - sale_timestamp
        )) AS time_diff_seconds
    FROM
        SalesWithTimestamps
)
SELECT
    year,
    CONCAT(
        'hours: ', FLOOR(AVG(time_diff_seconds) / 3600), ', ',
        'minutes: ', FLOOR((AVG(time_diff_seconds) % 3600) / 60), ', ',
        'seconds: ', FLOOR(AVG(time_diff_seconds) % 60), ', ',
        'milliseconds: ', FLOOR((AVG(time_diff_seconds) % 1) * 1000)
    ) AS actual_time_taken
FROM
    TimeDifferences
GROUP BY
    year
ORDER BY
    year;
