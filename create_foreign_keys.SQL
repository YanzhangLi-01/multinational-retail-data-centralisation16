-- Add foreign key to dim_date_times
ALTER TABLE orders_table
ADD CONSTRAINT fk_date_uuid FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid);

-- Add foreign key to dim_users
ALTER TABLE orders_table
ADD CONSTRAINT fk_user_uuid FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid);
-- Check Non-matching user_uuid
SELECT DISTINCT(ord.user_uuid)
FROM orders_table ord
WHERE NOT EXISTS 
(SELECT 1 FROM dim_users du
 WHERE du.user_uuid = ord.user_uuid);
-- Deleting Rows with Non-matching user_uuid using transaction
BEGIN;
DELETE FROM orders_table
WHERE user_uuid IN (
    SELECT DISTINCT ord.user_uuid
    FROM orders_table ord
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_users du
        WHERE du.user_uuid = ord.user_uuid
    )
);
COMMIT;

-- Add foreign key to dim_card_details
ALTER TABLE orders_table
ADD CONSTRAINT fk_card_number FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number);
-- Check Non-matching card_number
SELECT DISTINCT(ord.card_number)
FROM orders_table ord
WHERE NOT EXISTS 
(SELECT 1 FROM dim_card_details du
 WHERE du.card_number = ord.card_number);
-- Deleting Rows with Non-matching card_number using transaction
BEGIN;

DELETE FROM orders_table
WHERE card_number IN (
    SELECT card_number
    FROM orders_table ord
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_card_details du
        WHERE du.card_number = ord.card_number
    )
);

COMMIT;

-- Add foreign key to dim_store_details
ALTER TABLE orders_table
ADD CONSTRAINT fk_store_code FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code);
-- Check Non-matching store_code
SELECT DISTINCT(ord.store_code)
FROM orders_table ord
WHERE NOT EXISTS 
(SELECT 1 FROM dim_store_details du
 WHERE du.store_code = ord.store_code);
-- Deleting Rows with Non-matching store_code using transaction
BEGIN;

DELETE FROM orders_table
WHERE store_code IN (
    SELECT store_code
    FROM orders_table ord
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_store_details du
        WHERE du.store_code = ord.store_code
    )
);

COMMIT;

-- Add foreign key to dim_products
ALTER TABLE orders_table
ADD CONSTRAINT fk_product_code FOREIGN KEY (product_code) REFERENCES dim_products(product_code);
-- Check Non-matching product_code
SELECT DISTINCT(ord.product_code)
FROM orders_table ord
WHERE NOT EXISTS 
(SELECT 1 FROM dim_products du
 WHERE du.product_code = ord.product_code);
-- Deleting Rows with Non-matching product_code using transaction
BEGIN;

DELETE FROM orders_table
WHERE product_code IN (
    SELECT product_code
    FROM orders_table ord
    WHERE NOT EXISTS (
        SELECT 1 FROM dim_products du
        WHERE du.product_code = ord.product_code
    )
);

COMMIT;


-- Check foreign keys in orders_table
SELECT *
FROM information_schema.table_constraints
WHERE table_name = 'orders_table' AND constraint_type = 'FOREIGN KEY';
