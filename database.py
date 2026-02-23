import aiosqlite
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                created_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                sessions INTEGER,
                package_key TEXT,
                design_id TEXT,
                custom_style_id INTEGER,
                amount REAL,
                status TEXT DEFAULT 'pending',
                invoice_id INTEGER,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (custom_style_id) REFERENCES custom_styles(id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS custom_styles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                example_text TEXT,
                style_description TEXT,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        try:
            await db.execute("ALTER TABLE orders ADD COLUMN invoice_id INTEGER")
        except Exception:
            pass
        await db.commit()

async def get_or_create_user(user_id: int, username: str | None, first_name: str | None):
    async with aiosqlite.connect(DB_PATH) as db:
        from datetime import datetime
        await db.execute(
            """INSERT OR IGNORE INTO users (user_id, username, first_name, created_at)
               VALUES (?, ?, ?, ?)""",
            (user_id, username, first_name, datetime.utcnow().isoformat()),
        )
        await db.execute(
            """UPDATE users SET username = ?, first_name = ? WHERE user_id = ?""",
            (username, first_name, user_id),
        )
        await db.commit()

async def save_custom_style(user_id: int, example_text: str, style_description: str) -> int:
    from datetime import datetime
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """INSERT INTO custom_styles (user_id, example_text, style_description, created_at)
               VALUES (?, ?, ?, ?)""",
            (user_id, example_text, style_description, datetime.utcnow().isoformat()),
        )
        await db.commit()
        return cursor.lastrowid

async def get_custom_style(style_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM custom_styles WHERE id = ?", (style_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

async def get_user_custom_styles(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM custom_styles WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]


# --- Заказы и оплата Crypto Pay ---

async def create_order_with_invoice(
    user_id: int, package_key: str, amount: float, invoice_id: int
) -> int:
    from datetime import datetime
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """INSERT INTO orders (user_id, package_key, amount, status, invoice_id, created_at)
               VALUES (?, ?, ?, 'pending_payment', ?, ?)""",
            (user_id, package_key, amount, invoice_id, datetime.utcnow().isoformat()),
        )
        await db.commit()
        return cursor.lastrowid


async def get_order_by_invoice_id(invoice_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM orders WHERE invoice_id = ?", (invoice_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def set_order_paid(order_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE orders SET status = 'paid' WHERE id = ?", (order_id,)
        )
        await db.commit()
