-- Step 1: Determing the maximum length for the required conlumn
SELECT MAX(LENGTH(month)) AS max_month_length FROM dim_date_times;

SELECT MAX(LENGTH(year)) AS max_year_length FROM dim_date_times;

SELECT MAX(LENGTH(day)) AS max_day_length FROM dim_date_times;

SELECT MAX(LENGTH(time_period)) AS max_time_period_length FROM dim_date_times;

-- Step 2: Update the data types of columns
ALTER TABLE dim_date_times
ALTER COLUMN month TYPE VARCHAR(10),
ALTER COLUMN year TYPE VARCHAR(10),
ALTER COLUMN day TYPE VARCHAR(10),
ALTER COLUMN time_period TYPE VARCHAR(10),
ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;