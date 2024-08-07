--Step 1: Determing the maximum length for the required conlumn

-- Determine the maximum length for store_code
SELECT MAX(LENGTH(store_code)) AS max_store_code_length FROM dim_store_details;

-- Determine the maximum length for country_code
SELECT MAX(LENGTH(country_code)) AS max_country_code_length FROM dim_store_details;

-- Determine the maximum length for locality
SELECT MAX(LENGTH(locality)) AS max_locality_length FROM dim_store_details;

-- Determine the maximum length for store_type
SELECT MAX(LENGTH(store_type)) AS max_store_type_length FROM dim_store_details;

-- Determine the maximum length for continent
SELECT MAX(LENGTH(continent)) AS max_continent_length FROM dim_store_details;

-- Step 2: Update column data types using ALTER COLUMN
ALTER TABLE dim_store_details
ALTER COLUMN longitude TYPE REAL USING longitude::REAL,
ALTER COLUMN locality TYPE VARCHAR(20),
ALTER COLUMN store_code TYPE VARCHAR(11),
ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::SMALLINT,
ALTER COLUMN opening_date TYPE DATE USING opening_date::DATE,
ALTER COLUMN store_type TYPE VARCHAR(11),
ALTER COLUMN latitude TYPE REAL USING latitude::REAL,
ALTER COLUMN country_code TYPE VARCHAR(2),
ALTER COLUMN continent TYPE VARCHAR(7);
