
import os
from unittest import TestCase
from unittest.mock import patch

class TestMockCredentials(TestCase):
    @patch.dict(os.environ, {
        'DISCORD_BOT_TOKEN': 'MTExMjM0NTY3ODkwMTIzNDU2.mock_token',
        'WALLET_KEYPAIR': '5KHw2RWVKxqCxqvzT6aj8AHNV9VDyPn9KCwLLzG89BJV',
        'WEBDRIVER_PATH': '/usr/local/bin/chromedriver',
        'SOLANA_ENDPOINT': 'https://api.devnet.solana.com',
        'RAPIDAPI_KEY': 'mock_rapid_api_key_12345',
        'SCRAPENINJA_API_KEY': 'mock_scrape_ninja_key_12345',
        'PERSONATOR_API_KEY': 'mock_personator_key_12345',
        'VIRTUAL_NUMBER_API_KEY': 'mock_virtual_number_key_12345',
        'FAKE_VALID_CC_DATA_GENERATOR_API_KEY': 'mock_cc_gen_key_12345',
        'TEMP_MAIL_API_KEY': 'mock_temp_mail_key_12345',
        'PROXY_API_KEY': 'mock_proxy_key_12345',
        'API_KEY_SUBSCRIPTION': 'mock_subscription_key_12345',
        'GEMINI_API_KEY': 'mock_gemini_key_12345'
    })
    def test_mock_credentials(self):
        """Test that all mock credentials are properly set"""
        self.assertEqual(os.getenv('DISCORD_BOT_TOKEN'), 'MTExMjM0NTY3ODkwMTIzNDU2.mock_token')
        self.assertEqual(os.getenv('WALLET_KEYPAIR'), '5KHw2RWVKxqCxqvzT6aj8AHNV9VDyPn9KCwLLzG89BJV')
        self.assertEqual(os.getenv('RAPIDAPI_KEY'), 'mock_rapid_api_key_12345')
        self.assertEqual(os.getenv('SCRAPENINJA_API_KEY'), 'mock_scrape_ninja_key_12345')
        self.assertEqual(os.getenv('PERSONATOR_API_KEY'), 'mock_personator_key_12345')
        self.assertEqual(os.getenv('VIRTUAL_NUMBER_API_KEY'), 'mock_virtual_number_key_12345')
        self.assertEqual(os.getenv('FAKE_VALID_CC_DATA_GENERATOR_API_KEY'), 'mock_cc_gen_key_12345')
        self.assertEqual(os.getenv('TEMP_MAIL_API_KEY'), 'mock_temp_mail_key_12345')
        self.assertEqual(os.getenv('PROXY_API_KEY'), 'mock_proxy_key_12345')
        self.assertEqual(os.getenv('API_KEY_SUBSCRIPTION'), 'mock_subscription_key_12345')
        self.assertEqual(os.getenv('GEMINI_API_KEY'), 'mock_gemini_key_12345')

    def test_missing_credentials(self):
        """Test handling of missing credentials"""
        with patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(os.getenv('DISCORD_BOT_TOKEN'))
            self.assertIsNone(os.getenv('WALLET_KEYPAIR'))
            self.assertIsNone(os.getenv('RAPIDAPI_KEY'))

if __name__ == '__main__':
    unittest.main()
