import sqlite3
from pathlib import Path

def create_sample_database():
    """Create a sample SQLite database for testing."""

    db_path = Path("data/sample.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            signup_date DATE,
            plan TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product TEXT,
            amount REAL,
            purchase_date DATE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Insert sample data
    users = [
        (1, 'Alice Johnson', 'alice@example.com', '2024-01-15', 'premium'),
        (2, 'Bob Smith', 'bob@example.com', '2024-02-20', 'basic'),
        (3, 'Carol White', 'carol@example.com', '2024-03-10', 'premium'),
        (4, 'David Brown', 'david@example.com', '2024-04-05', 'basic'),
    ]

    cursor.executemany(
        "INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?)",
        users
    )

    purchases = [
        (1, 1, 'ML Course', 99.99, '2024-01-20'),
        (2, 1, 'Data Engineering Book', 49.99, '2024-02-15'),
        (3, 2, 'Python Course', 79.99, '2024-03-01'),
        (4, 3, 'AI Toolkit', 149.99, '2024-03-15'),
        (5, 3, 'Cloud Computing Course', 89.99, '2024-04-01'),
    ]

    cursor.executemany(
        "INSERT OR REPLACE INTO purchases VALUES (?, ?, ?, ?, ?)",
        purchases
    )

    conn.commit()
    conn.close()

    print(f"✓ Sample database created at: {db_path}")
    print(f"  - {len(users)} users")
    print(f"  - {len(purchases)} purchases")

if __name__ == "__main__":
    create_sample_database()