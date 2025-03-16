-- Users table (stores pet owners, veterinarians, and other staff)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
);