CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    threshold INT NOT NULL
);

CREATE TABLE inventory (
    product_id INT PRIMARY KEY,
    current_stock INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE vendors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    price FLOAT NOT NULL,
    distance FLOAT NOT NULL,
    lead_time INT NOT NULL
);

CREATE TABLE purchase_orders (
    id SERIAL PRIMARY KEY,
    vendor_id INT,
    status TEXT,
    po_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vendor_id) REFERENCES vendors(id)
);

CREATE TABLE logistics_updates (
    id SERIAL PRIMARY KEY,
    po_id INT,
    status TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (po_id) REFERENCES purchase_orders(id)
);

CREATE TABLE IF NOT EXISTS vendor_reputation (
    id SERIAL PRIMARY KEY,
    vendor_id INT,
    issue TEXT,
    rating FLOAT
);

-- Useful indexes
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_po_vendor ON purchase_orders(vendor_id);
CREATE INDEX idx_logistics_po ON logistics_updates(po_id);