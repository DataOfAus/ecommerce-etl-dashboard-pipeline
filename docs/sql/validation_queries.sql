
-- A quick check of the last 5 lines to confirm format

SELECT * FROM products_50k
ORDER BY id
OFFSET 49995;

-- Counts the no. of rows in the generated table to confirm all 50k lines transferred

SELECT COUNT(*) FROM products_50k;
