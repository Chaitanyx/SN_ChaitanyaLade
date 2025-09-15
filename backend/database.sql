CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL, -- e.g., admin, family, guest
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    token TEXT UNIQUE,
    expires_at TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE access_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    folder_path TEXT,
    permissions TEXT, -- e.g., read, write
    valid_until TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
