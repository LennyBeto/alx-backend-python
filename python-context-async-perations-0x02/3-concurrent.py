import asyncio
import aiosqlite # Asynchronous SQLite library

async def async_fetch_users():
    """Fetch all users from the database"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users') as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    """Fetch users older than 40 from the database"""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users WHERE age > ?', (40,)) as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    """Execute both queries concurrently"""
    return await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

async def main():
    """Main async function to run the queries"""
    all_users, older_users = await fetch_concurrently()
    print(f"Total users: {len(all_users)}")
    print(f"Users over 40: {len(older_users)}")
    print("\nSample older users:")
    for user in older_users[:5]:  # Print first 5 older users
        print(user)

if __name__ == '__main__':
    asyncio.run(main())
