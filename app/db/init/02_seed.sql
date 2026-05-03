-- Product
INSERT INTO products (name, threshold)
VALUES ('Shampoo Bottle 200ml', 100);

-- Inventory (LOW STOCK to trigger system)
INSERT INTO inventory (product_id, current_stock)
VALUES (1, 40);

-- Vendors (price vs distance vs lead_time tradeoff)
INSERT INTO vendors (name, price, distance, lead_time) VALUES
('Vendor A - Cheap but far', 80, 1200, 7),
('Vendor B - Balanced', 95, 400, 4),
('Vendor C - Fast but expensive', 120, 100, 2),
('Vendor D - Risky (delays history)', 85, 300, 10);


INSERT INTO vendor_reputation (vendor_id, issue, rating) VALUES
(1, 'Frequent delivery delays', 2.5),
(1, 'Good pricing but inconsistent quality', 3.0),
(2, 'Reliable and on-time delivery', 4.5),
(2, 'Strong quality consistency', 4.2),
(3, 'Expensive but premium quality', 4.0),
(3, 'Long lead time', 3.2);