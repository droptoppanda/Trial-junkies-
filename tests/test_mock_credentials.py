
import os
from unittest import TestCase
from unittest.mock import patch

class TestMockCredentials(TestCase):
    @patch.dict(os.environ, {
        'DISCORD_BOT_TOKEN': 'MTExMjM0NTY3ODkwMTIzNDU2.mock_token',
        'WALLET_KEYPAIR': '5KHw2RWVKxqCxqvzT6aj8AHNV9VDyPn9KCwLLzG89BJV'
    })
    def test_mock_credentials(self):
        self.assertEqual(os.getenv('DISCORD_BOT_TOKEN'), 'MTExMjM0NTY3ODkwMTIzNDU2.mock_token')
        self.assertEqual(os.getenv('WALLET_KEYPAIR'), '5KHw2RWVKxqCxqvzT6aj8AHNV9VDyPn9KCwLLzG89BJV')

if __name__ == '__main__':
    unittest.main()
