TRUNCATE TABLE
    refunds,
    payments,
    order_items,
    orders,
    products,
    customers
RESTART IDENTITY CASCADE;

INSERT INTO customers (customer_name, city, member_level, registered_at) VALUES
    ('Alice', 'Shanghai', 'gold', '2025-12-10'),
    ('Bob', 'Beijing', 'silver', '2026-01-05'),
    ('Cindy', 'Shanghai', 'platinum', '2025-10-18'),
    ('David', 'Shenzhen', 'bronze', '2026-02-01'),
    ('Eva', 'Beijing', 'gold', '2025-11-22'),
    ('Frank', 'Guangzhou', 'silver', '2026-01-19'),
    ('Grace', 'Hangzhou', 'platinum', '2025-09-30'),
    ('Henry', 'Chengdu', 'bronze', '2026-03-08');

INSERT INTO products (product_name, category, cost_price, list_price) VALUES
    ('AI Keyboard', 'electronics', 220.00, 399.00),
    ('Smart Mug', 'electronics', 80.00, 159.00),
    ('Data Notebook', 'stationery', 18.00, 39.00),
    ('SQL Hoodie', 'apparel', 95.00, 199.00),
    ('Vector Backpack', 'apparel', 130.00, 299.00),
    ('Cloud Course', 'education', 60.00, 299.00),
    ('Analytics Book', 'education', 45.00, 129.00);

INSERT INTO orders (customer_id, order_no, order_status, ordered_at) VALUES
    (1, 'OD20260501001', 'completed', '2026-05-01 10:20:00'),
    (2, 'OD20260501002', 'completed', '2026-05-01 11:15:00'),
    (3, 'OD20260502001', 'completed', '2026-05-02 09:30:00'),
    (4, 'OD20260502002', 'cancelled', '2026-05-02 14:05:00'),
    (5, 'OD20260503001', 'completed', '2026-05-03 16:10:00'),
    (6, 'OD20260504001', 'completed', '2026-05-04 12:45:00'),
    (7, 'OD20260505001', 'completed', '2026-05-05 19:22:00'),
    (1, 'OD20260506001', 'completed', '2026-05-06 08:55:00'),
    (8, 'OD20260507001', 'paid', '2026-05-07 20:15:00'),
    (3, 'OD20260508001', 'completed', '2026-05-08 13:05:00'),
    (5, 'OD20260425001', 'completed', '2026-04-25 15:40:00'),
    (6, 'OD20260428001', 'completed', '2026-04-28 09:50:00');

INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount_amount) VALUES
    (1, 1, 1, 399.00, 30.00),
    (1, 3, 2, 39.00, 0.00),
    (2, 4, 1, 199.00, 20.00),
    (2, 7, 1, 129.00, 0.00),
    (3, 6, 1, 299.00, 50.00),
    (3, 2, 2, 159.00, 20.00),
    (4, 5, 1, 299.00, 0.00),
    (5, 1, 1, 399.00, 0.00),
    (5, 6, 1, 299.00, 40.00),
    (6, 2, 3, 159.00, 30.00),
    (6, 3, 5, 39.00, 0.00),
    (7, 5, 1, 299.00, 20.00),
    (7, 7, 2, 129.00, 0.00),
    (8, 6, 2, 299.00, 60.00),
    (9, 4, 2, 199.00, 0.00),
    (10, 1, 1, 399.00, 25.00),
    (10, 2, 1, 159.00, 0.00),
    (11, 7, 3, 129.00, 30.00),
    (12, 5, 1, 299.00, 0.00),
    (12, 3, 4, 39.00, 0.00);

INSERT INTO payments (order_id, payment_method, payment_status, paid_amount, paid_at) VALUES
    (1, 'wechat', 'paid', 447.00, '2026-05-01 10:25:00'),
    (2, 'alipay', 'paid', 308.00, '2026-05-01 11:18:00'),
    (3, 'credit_card', 'paid', 547.00, '2026-05-02 09:35:00'),
    (4, 'wechat', 'failed', 0.00, NULL),
    (5, 'bank_transfer', 'paid', 658.00, '2026-05-03 16:20:00'),
    (6, 'alipay', 'paid', 642.00, '2026-05-04 12:50:00'),
    (7, 'wechat', 'refunded', 537.00, '2026-05-05 19:25:00'),
    (8, 'credit_card', 'paid', 538.00, '2026-05-06 09:01:00'),
    (9, 'wechat', 'paid', 398.00, '2026-05-07 20:20:00'),
    (10, 'alipay', 'paid', 533.00, '2026-05-08 13:10:00'),
    (11, 'credit_card', 'paid', 357.00, '2026-04-25 15:45:00'),
    (12, 'wechat', 'paid', 455.00, '2026-04-28 09:55:00');

INSERT INTO refunds (order_id, refund_reason, refund_amount, refunded_at) VALUES
    (7, 'size mismatch', 120.00, '2026-05-06 10:30:00'),
    (10, 'late delivery', 80.00, '2026-05-09 09:20:00');
