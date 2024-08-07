--Step 1: Determing the maximum length for the required conlumn

-- Determine the maximum length for country_code
SELECT MAX(LENGTH(country_code)) AS max_country_code_length FROM dim_users;

-- Step 2: Update column data types using ALTER COLUMN
ALTER TABLE dim_users
ALTER COLUMN first_name TYPE VARCHAR(255),
ALTER COLUMN last_name TYPE VARCHAR(255),
ALTER COLUMN date_of_birth TYPE DATE USING date_of_birth::DATE,
ALTER COLUMN country_code TYPE VARCHAR(3), 
ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
ALTER COLUMN join_date TYPE DATE USING join_date::DATE;