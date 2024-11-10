CREATE TABLE IF NOT EXISTS config (
    id SERIAL PRIMARY KEY,
    status_value INTEGER NOT NULL
);


INSERT INTO config (status_value) VALUES (100);
