import aiosqlite
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'new.db')


async def db_start():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS profile(
                user_id TEXT PRIMARY KEY, 
                level TEXT,
                photo TEXT, 
                age TEXT, 
                description TEXT, 
                name TEXT
            )
        """)
        await db.commit()
        print("Database and table created successfully.")


async def create_profile(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT 1 FROM profile WHERE user_id = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()
            if not user:
                await db.execute(
                    "INSERT INTO profile (user_id, level, photo, age, description, name) VALUES(?, ?, ?, ?, ?, ?)",
                    (user_id, '', '', '', '', ''))
                await db.commit()
                print(f"Profile created for user {user_id}.")


async def edit_profile(state, user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        data = await state.get_data()
        await db.execute("""
            UPDATE profile 
            SET level = ?, photo = ?, age = ?, description = ?, name = ?
            WHERE user_id = ?
        """, (data['level'], data['photo'], data['age'], data['description'], data['name'], user_id))
        await db.commit()
        print(f"Profile updated for user {user_id}.")


async def isRegistered(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT 1 FROM profile WHERE user_id = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()
            return user is not None


async def get_profile(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT level, photo, name, age, description FROM profile WHERE user_id = ?",
                              (user_id,)) as cursor:
            return await cursor.fetchone()
