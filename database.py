import aiosqlite
from config import config

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    async def create_tables(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    code TEXT PRIMARY KEY,
                    file_id TEXT NOT NULL,
                    description TEXT
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    channel_id TEXT PRIMARY KEY,
                    channel_link TEXT NOT NULL,
                    channel_name TEXT NOT NULL
                )
            """)
            await db.commit()

    async def add_user(self, user_id: int):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
            await db.commit()

    async def get_users_count(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT COUNT(*) FROM users") as cursor:
                result = await cursor.fetchone()
                return result[0] if result else 0

    async def add_video(self, code: str, file_id: str, description: str = None):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "INSERT OR REPLACE INTO videos (code, file_id, description) VALUES (?, ?, ?)",
                (code, file_id, description)
            )
            await db.commit()

    async def get_video(self, code: str):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT file_id, description FROM videos WHERE code = ?", (code,)) as cursor:
                return await cursor.fetchone()

    async def delete_video(self, code: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DELETE FROM videos WHERE code = ?", (code,))
            await db.commit()

    async def get_all_videos(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT code, description FROM videos") as cursor:
                return await cursor.fetchall()

    async def add_channel(self, channel_id: str, channel_link: str, channel_name: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "INSERT OR REPLACE INTO channels (channel_id, channel_link, channel_name) VALUES (?, ?, ?)",
                (channel_id, channel_link, channel_name)
            )
            await db.commit()

    async def get_channels(self):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT channel_id, channel_link, channel_name FROM channels") as cursor:
                return await cursor.fetchall()

    async def delete_channel(self, channel_id: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DELETE FROM channels WHERE channel_id = ?", (channel_id,))
            await db.commit()

db = Database(config.DB_NAME)
