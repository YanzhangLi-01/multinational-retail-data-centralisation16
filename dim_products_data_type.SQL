-- Step 1: Rename the removed Column
ALTER TABLE dim_products
RENAME COLUMN removed TO still_available;

-- Step 2: Determing the maximum length for the required conlumn
SELECT MAX(LENGTH("EAN")) AS max_EAN_length FROM dim_products;

SELECT MAX(LENGTH(product_code)) AS max_product_code_length FROM dim_products;

SELECT MAX(LENGTH(weight_class)) AS max_weight_class_length FROM dim_products;

-- Step 3: Change data type in column to Boolean.
UPDATE dim_products
SET still_available = CASE
    WHEN still_available = 'Still_available' THEN 'TRUE'
    WHEN still_available = 'Removed' THEN 'FALSE'
    ELSE 'TRUE'  -- Optional: handle any unexpected values
END;

-- Step 4: Change the Data Types of Columns
ALTER TABLE dim_products
ALTER COLUMN product_price TYPE FLOAT USING product_price::FLOAT,
ALTER COLUMN weight TYPE FLOAT USING weight::FLOAT,
ALTER COLUMN "EAN" TYPE VARCHAR(17),
ALTER COLUMN product_code TYPE VARCHAR(11),
ALTER COLUMN date_added TYPE DATE USING date_added::DATE,
ALTER COLUMN uuid TYPE UUID USING uuid::UUID,
ALTER COLUMN still_available TYPE BOOLEAN USING still_available::BOOLEAN,
ALTER COLUMN weight_class TYPE VARCHAR(14);
