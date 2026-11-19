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

CREATE TABLE forecast_decisions (
    id          SERIAL PRIMARY KEY,
    thread_id   TEXT NOT NULL,
    method      TEXT NOT NULL,
    forecast    JSONB NOT NULL,
    reason      TEXT,
    attempts    INTEGER NOT NULL,
    approved    BOOLEAN NOT NULL,
    decided_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);