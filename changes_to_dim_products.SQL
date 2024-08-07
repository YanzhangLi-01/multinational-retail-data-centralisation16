-- Task 1: Remove the £ Character from the product_price Column
-- Step 1: Remove the £ Character and Convert to Numeric:
UPDATE dim_products
SET product_price = REPLACE(product_price, '£', '')::NUMERIC;
-- Step 2: Change the Column Data Type
ALTER TABLE dim_products
ALTER COLUMN product_price TYPE NUMERIC USING product_price::NUMERIC;

-- Task 2: Add the weight_class Column
-- Step 1: Add the New Column:
ALTER TABLE dim_products
ADD COLUMN weight_class VARCHAR(20);
-- Step 2: Update the weight_class Column Based on Weight Ranges:
UPDATE dim_products
SET weight_class = CASE
    WHEN weight < 2 THEN 'Light'
    WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
    WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
    WHEN weight >= 140 THEN 'Truck_Required'
    ELSE 'Unknown'  -- Optional: handle unexpected values
END;