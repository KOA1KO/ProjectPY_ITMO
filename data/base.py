import random

import aiosqlite
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'new.db')


async def db_start():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS profile(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT, 
                level TEXT,
                photo TEXT, 
                age TEXT, 
                description TEXT, 
                name TEXT,
                is_searching INTEGER DEFAULT 0,
                chatting_with INTEGER DEFAULT None
            )
        """)
        await db.commit()
        print("Database and table created successfully.")


async def create_profile(user_id, level='', photo='', age='', description='', name='', is_searching=0,
                         chatting_with=None):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT 1 FROM profile WHERE user_id = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()
            if not user:
                await db.execute(
                    "INSERT INTO profile (user_id, level, photo, age, description, name, is_searching, chatting_with) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_id, level, photo, age, description, name, is_searching, chatting_with))
                await db.commit()
                print(f"Profile created for user {user_id}.")


async def edit_profile(state, user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        data = await state.get_data()
        await db.execute("""
            UPDATE profile 
            SET level = ?, photo = ?, age = ?, description = ?, name = ?
            WHERE user_id = ?
        """, (
            data['level'], data['photo'], data['age'], data['description'], data['name'], user_id))
        await db.commit()
        print(f"Profile updated for user {user_id}.")
        print((data['level'], data['photo'], data['age'], data['description'], data['name'], user_id))


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


async def is_someone_searching(level, user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
                "SELECT user_id, level, photo, name, age, description, is_searching FROM profile WHERE level = ? AND user_id != ? AND is_searching = 1",
                (level, user_id,)) as cursor:
            results = await cursor.fetchall()
            if results:
                return random.choice(results)
            else:
                return None


async def get_chatting_with_id(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT chatting_with FROM profile WHERE user_id = ?", (user_id,)) as cursor:
            result = await cursor.fetchone()
            if result:
                other_user_id = result[0]  # Получаем значение из кортежа
                print(f"{user_id} is chatting with user {other_user_id}.")
                return other_user_id
            else:
                print(f"{user_id} is not chatting with anyone.")
                return None


async def update_is_searching(user_id, is_searching, with_who):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Update the user
        await db.execute("UPDATE profile SET is_searching = ?, chatting_with = ? WHERE user_id = ?",
                         (is_searching, with_who, user_id))
        await db.commit()
        print(f"is_searching updated to {is_searching} for user {user_id}.")


async def update_level(user_id, level):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE profile 
            SET level = ?
            WHERE user_id = ?
        """, (level, user_id))
        await db.commit()
        print(f"Level updated to {level} for user {user_id}.")
