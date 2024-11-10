CREATE TABLE IF NOT EXISTS config (
    id SERIAL PRIMARY KEY,
    status_value INTEGER NOT NULL,
    is_update_enabled BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO config (status_value, is_update_enabled) VALUES (100, FALSE);
