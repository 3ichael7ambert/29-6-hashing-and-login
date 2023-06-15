CREATE DATABASE users_db;

\c users_db

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL
);

CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    content TEXT,
    username VARCHAR(50),
    FOREIGN KEY (username) REFERENCES users (username)
);
