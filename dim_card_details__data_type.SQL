-- Step 1: Determing the maximum length for the required conlumn
SELECT MAX(LENGTH(card_number)) AS max_card_number_length FROM dim_card_details;

SELECT MAX(LENGTH(expiry_date)) AS max_expiry_date_length FROM dim_card_details;

-- Step 2: Update the data types of columns
ALTER TABLE dim_card_details
ALTER COLUMN card_number TYPE VARCHAR(22),  -- or another length if needed
ALTER COLUMN expiry_date TYPE VARCHAR(5),   -- or another length if needed
ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::DATE;

