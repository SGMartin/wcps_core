import asyncio
import aiomysql

async def fetch_player_data(player_id, pool):
    try:
        # Get a connection from the pool
        async with pool.acquire() as conn:
            # Create a cursor
            async with conn.cursor() as cursor:
                # Execute a SELECT query with a parameterized WHERE clause
                await cursor.execute("SELECT * FROM players WHERE id = %s", (player_id,))

                # Fetch the results
                result = await cursor.fetchone()

                # Close the cursor
                cursor.close()

            # Return the connection to the pool
            conn.close()
    except (aiomysql.PoolError, aiomysql.ConnectionError) as e:
        # Handle errors and exceptions
        print(f"Error fetching player data: {e}")
        result = None

    return result


"""
import asyncio
import database

async def main():
    # Create a connection pool
    pool = await aiomysql.create_pool(host='localhost', user='user', password='password',
                                      db='game_db', loop=loop)

    # Fetch player data using the connection pool
    player_data = await database.fetch_player_data(1, pool)
    print(player_data)

    # Close the connection pool
    pool.close()
    await pool.wait_closed()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
"""