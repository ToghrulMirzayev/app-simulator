CREATE TABLE IF NOT EXISTS config (
    id SERIAL PRIMARY KEY,
    status_value INTEGER NOT NULL,
    is_update_enabled BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO config (status_value, is_update_enabled) VALUES (100, FALSE);

CREATE TABLE IF NOT EXISTS phrases (
    id SERIAL PRIMARY KEY,
    ru_text TEXT,
    en_text TEXT
);

INSERT INTO phrases (ru_text, en_text) VALUES
('Счастье — это выбор', 'Happiness is a choice'),
('Время — деньги', 'Time is money');

CREATE TABLE IF NOT EXISTS language_config (
    id SERIAL PRIMARY KEY,
    language VARCHAR(2) NOT NULL
);

INSERT INTO language_config (language) VALUES ('RU');
