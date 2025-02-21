
import unittest
from unittest.mock import patch, mock_open
import os
from dotenv import load_dotenv

class TestEnvLoader(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='RAPIDAPI_KEY=test_key\nSOLANA_ENDPOINT=test_endpoint')
    def test_env_loading(self, mock_file):
        """Test that environment variables are loaded correctly from .env"""
        load_dotenv()
        self.assertEqual(os.getenv('RAPIDAPI_KEY'), 'test_key')
        self.assertEqual(os.getenv('SOLANA_ENDPOINT'), 'test_endpoint')

    def test_required_env_vars(self):
        """Test that all required environment variables are present"""
        required_vars = [
            'RAPIDAPI_KEY',
            'WALLET_KEYPAIR',
            'SOLANA_ENDPOINT',
            'DISCORD_BOT_TOKEN',
            'GEMINI_API_KEY'
        ]
        
        for var in required_vars:
            self.assertIsNotNone(os.getenv(var), f"Required environment variable {var} is missing")

if __name__ == '__main__':
    unittest.main()
