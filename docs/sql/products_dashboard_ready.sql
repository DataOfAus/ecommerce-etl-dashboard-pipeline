CREATE OR REPLACE VIEW products_dashboard_ready AS
WITH base AS (
  SELECT 
    id,
    title,
    category,
    price,
    description,
    "rating.rate" AS rating_rate,
    "rating.count" AS rating_count,
    extracted_at
  FROM products_transformed
),
category_summary AS (
  SELECT 
    category,
    COUNT(*) AS product_count,
    ROUND(AVG(price)::numeric, 2) AS avg_price,
    ROUND(AVG(rating_rate)::numeric, 2) AS avg_rating,
    SUM(rating_count) AS total_ratings
  FROM base
  GROUP BY category
),
top_products AS (
  SELECT 
    id,
    title,
    category,
    price,
    rating_rate,
    rating_count
  FROM base
  ORDER BY rating_rate DESC, rating_count DESC
  LIMIT 10
),
final AS (
  SELECT 
    b.*,
    cs.product_count,
    cs.avg_price,
    cs.avg_rating,
    cs.total_ratings
  FROM base b
  LEFT JOIN category_summary cs ON b.category = cs.category
)
SELECT * FROM final;



