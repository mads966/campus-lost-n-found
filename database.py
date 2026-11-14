import sqlite3

DB_NAME = "lost_and_found.db"

def connect(db_name=DB_NAME):
    return sqlite3.connect(db_name)

def initialize_database(db_name=DB_NAME):
    with connect(db_name) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                type TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open'
            )
        """)

def add_item(name, description, location, item_type,
             db_name=DB_NAME):
    if not all([name.strip(), description.strip(),
                location.strip()]):
        raise ValueError("All fields are required")

    if item_type not in ("Lost", "Found"):
        raise ValueError("Type must be Lost or Found")

    with connect(db_name) as conn:
        cursor = conn.execute("""
            INSERT INTO items
            (name, description, location, type)
            VALUES (?, ?, ?, ?)
        """, (name, description, location, item_type))
        return cursor.lastrowid

def search_items(keyword, db_name=DB_NAME):
    with connect(db_name) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT * FROM items
            WHERE name LIKE ? OR description LIKE ?
            OR location LIKE ?
        """, (f"%{keyword}%",) * 3).fetchall()
        return [dict(row) for row in rows]

def update_status(item_id, status, db_name=DB_NAME):
    if status not in ("Open", "Returned"):
        raise ValueError("Invalid status")

    with connect(db_name) as conn:
        cursor = conn.execute("""
            UPDATE items SET status = ?
            WHERE id = ?
        """, (status, item_id))
        return cursor.rowcount > 0
