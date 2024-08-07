-- Step 1: Determing the maximum length for the required conlumn

-- Determine the maximum length for card_number
SELECT MAX(LENGTH(card_number::TEXT)) AS max_card_number_length FROM orders_table;

-- Determine the maximum length for store_code
SELECT MAX(LENGTH(store_code::TEXT)) AS max_store_code_length FROM orders_table;

-- Determine the maximum length for product_code
SELECT MAX(LENGTH(product_code::TEXT)) AS max_product_code_length FROM orders_table;

-- Step 2: Update column data types using ALTER COLUMN
ALTER TABLE orders_table
ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID,
ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
ALTER COLUMN card_number TYPE VARCHAR(19),
ALTER COLUMN store_code TYPE VARCHAR(12),
ALTER COLUMN product_code TYPE VARCHAR(11),
ALTER COLUMN product_quantity TYPE SMALLINT;