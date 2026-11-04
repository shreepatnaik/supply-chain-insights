CREATE TABLE orders (
    order_item_id            INTEGER PRIMARY KEY,
    order_id                 INTEGER NOT NULL,
    order_date               TIMESTAMP NOT NULL,
    shipping_date            TIMESTAMP NOT NULL,
    days_shipping_real       INTEGER NOT NULL,
    days_shipping_scheduled  INTEGER NOT NULL,
    late_delivery_risk       BOOLEAN NOT NULL,
    delivery_status          TEXT NOT NULL,
    shipping_mode            TEXT NOT NULL,
    order_region             TEXT NOT NULL,
    market                   TEXT NOT NULL,
    category_name            TEXT NOT NULL,
    quantity                 INTEGER NOT NULL,
    sales                    NUMERIC(10, 2) NOT NULL,
    order_status             TEXT NOT NULL
);