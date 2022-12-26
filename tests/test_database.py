import unittest
import asyncio
import aiomysql

class TestFetchPlayerData(unittest.TestCase):
    def setUp(self):
        # Create an event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Create a connection pool
        self.pool = self.loop.run_until_complete(aiomysql.create_pool(host='localhost', user='user', password='password',
                                                                      db='game_db', loop=self.loop))

    def tearDown(self):
        # Close the connection pool
        self.pool.close()
        self.loop.run_until_complete(self.pool.wait_closed())

        # Close the event loop
        self.loop.close()

    def test_fetch_player_data(self):
        # Test fetching player data
        result = self.loop.run_until_complete(fetch_player_data(1, self.pool))
        self.assertIsNotNone(result)

    def test_fetch_invalid_player(self):
        # Test fetching player data for an invalid player ID
        result = self.loop.run_until_complete(fetch_player_data(-1, self.pool))
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()