-- Add primary key to dim_date_times
ALTER TABLE dim_date_times
ADD CONSTRAINT pk_date_uuid PRIMARY KEY (date_uuid);

-- Add primary key to dim_users
ALTER TABLE dim_users
ADD CONSTRAINT pk_user_uuid PRIMARY KEY (user_uuid);

-- Add primary key to dim_card_details
ALTER TABLE dim_card_details
ADD CONSTRAINT pk_card_number PRIMARY KEY (card_number);

-- Add primary key to dim_store_details
ALTER TABLE dim_store_details
ADD CONSTRAINT pk_store_code PRIMARY KEY (store_code);

-- Add primary key to dim_products
ALTER TABLE dim_products
ADD CONSTRAINT pk_product_code PRIMARY KEY (product_code);

-- Check primary keys in dim_date_times
SELECT *
FROM information_schema.table_constraints
WHERE table_name = 'dim_date_times' AND constraint_type = 'PRIMARY KEY';

-- Check primary keys in dim_users
SELECT *
FROM information_schema.table_constraints
WHERE table_name = 'dim_users' AND constraint_type = 'PRIMARY KEY';

-- Check primary keys in dim_card_details
SELECT *
FROM information_schema.table_constraints
WHERE table_name = 'dim_card_details' AND constraint_type = 'PRIMARY KEY';

-- Check primary keys in dim_store_details
SELECT *
FROM information_schema.table_constraints
WHERE table_name = 'dim_store_details' AND constraint_type = 'PRIMARY KEY';

-- Check primary keys in dim_products
SELECT *
FROM information_schema.table_constraints
WHERE table_name = 'dim_products' AND constraint_type = 'PRIMARY KEY';
