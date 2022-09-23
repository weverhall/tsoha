CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE rides (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);