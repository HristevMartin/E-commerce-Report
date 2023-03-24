import os

db_name = os.getenv('DB_NAME')

if not db_name:
    raise ValueError('DB_NAME is missing')

QUERY_GET_TOTAL_NUMBER_OF_ITEMS_SOLD_PER_DAY = """
    SELECT SUM(quantity) as items_sold
    FROM OrderLine
    JOIN `Order` ON OrderLine.order_id = `Order`.id
    WHERE DATE(`Order`.created_at) = :date;
"""

QUERY_GET_TOTAL_ORDERS_PER_CUSOTOMER_DAILY = f"""
    SELECT COUNT(DISTINCT customer_id)
    as total_customers FROM {db_name}.Order
    WHERE DATE(created_at) = :date;
"""

QUERY_GET_TOTAL_DISCOUNT_GIVEN_PER_DAY = f"""
    SELECT SUM(discounted_amount) AS total_discount_amount
    FROM OrderLine
    JOIN {db_name}.Order ON {db_name}.Order.id = OrderLine.order_id
    WHERE DATE(created_at) = :date;

"""

QUERY_GET_AVERAGE_DISCOUNTRATE_ON_ITEM_SOLD_PER_DAY = f"""
    SELECT AVG(ol.discount_rate) as avg_discount_rate
    FROM {db_name}.Order o
    JOIN OrderLine ol ON o.id = ol.order_id
    WHERE DATE(o.created_at) = :date

"""

QUERY_AVERAGE_ORDER_TOTAL_PER_DAY = f"""
 SELECT AVG(total_amount) as avg_order_total
    FROM (
  SELECT o.id, SUM(ol.discounted_amount + ol.vat_amount) as total_amount
  FROM {db_name}.Order o
  JOIN OrderLine ol ON o.id = ol.order_id
  WHERE DATE(o.created_at) = :date
  GROUP BY o.id
) as order_totals
"""

QUERY_GET_TOTAL_AMOUNT_OF_COMMISSIONS_GENERATED_PER_DAY = f"""
SELECT SUM(vc.rate * order_totals.total_amount) as total_commissions
FROM (
  SELECT o.vendor_id, SUM(ol.discounted_amount + ol.vat_amount) as total_amount
  FROM {db_name}.Order o
  JOIN OrderLine ol ON o.id = ol.order_id
  WHERE DATE(o.created_at)= :date
  GROUP BY o.id, o.vendor_id
) as order_totals
JOIN VendorCommissions vc ON DATE(vc.date) = '2019-08-03' AND order_totals.vendor_id = vc.vendor_id

"""

QUERY_GET_TOTAL_AMOUNT_OF_COMMISSION_PER_PROMOTION_PER_DAY = f"""
    SELECT pp.promotion_id, SUM(vc.rate * ol.discounted_amount) as total_commissions
    FROM OrderLine ol
    JOIN (
      SELECT id, vendor_id, customer_id
      FROM {db_name}.Order
      WHERE DATE(created_at) = :date
    ) as o ON ol.order_id = o.id
    JOIN (
      SELECT product_id, promotion_id
      FROM ProductPromotion
      WHERE DATE(date) = :date
    ) as pp ON ol.product_id = pp.product_id
    JOIN VendorCommissions vc ON DATE(vc.date) = :date AND vc.vendor_id = o.vendor_id
    GROUP BY pp.promotion_id
"""

QUERY_GET_COMMISION_PER_CATEGORY = """
    SELECT p.id AS promotion_id, SUM(ol.total_amount * vc.rate) AS commission_amount
    FROM ProductPromotion pp
    JOIN OrderLine ol ON pp.product_id = ol.product_id
    JOIN Promotion p ON pp.promotion_id = p.id
    JOIN Product pr ON pp.product_id = pr.id
    JOIN `Order` o ON ol.order_id = o.id
    JOIN VendorCommissions vc ON o.vendor_id = vc.vendor_id AND DATE(o.created_at) = vc.date
    WHERE pp.date = :date
    GROUP BY p.id;
"""

QUERY_CREATE_ORDER_TABLE = """
    CREATE TABLE `Order` (
      `id` int NOT NULL,
      `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
      `vendor_id` int DEFAULT NULL,
      `customer_id` int DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

QUERY_CREATE_ORDERLINE_TABLE = """
  CREATE TABLE `OrderLine` (
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `product_description` varchar(255) DEFAULT NULL,
  `product_price` decimal(10,2) DEFAULT NULL,
  `product_vat_rate` decimal(5,2) DEFAULT NULL,
  `discount_rate` decimal(5,2) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `full_price_amount` decimal(10,2) DEFAULT NULL,
  `discounted_amount` decimal(10,2) DEFAULT NULL,
  `vat_amount` decimal(10,2) DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

QUERY_CREATE_PRODUCT_TABLE = """
    CREATE TABLE `Product` (
    `id` int NOT NULL,
    `description` varchar(255) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

QUERY_CREATE_PROMOTION_TABLE = """
    CREATE TABLE `Promotion` (
    `id` int NOT NULL,
    `description` varchar(255) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

QUERY_CREATE_PRODUCT_PROMOTION_TABLE = """
       CREATE TABLE `ProductPromotion` (
      `date` varchar(128) NOT NULL,
      `product_id` int NOT NULL,
      `promotion_id` int NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

QUERY_CREATE_VendorCommision_TABLE = """
      CREATE TABLE `VendorCommissions` (
      `date` date NOT NULL,
      `vendor_id` int NOT NULL,
      `rate` decimal(5,2) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""
