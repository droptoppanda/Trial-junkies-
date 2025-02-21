
import unittest
from unittest.mock import patch, MagicMock
from solana_pay import SolanaPay

class TestSolanaPay(unittest.TestCase):
    def setUp(self):
        # Using valid test keypair from test_mock_credentials
        self.solana_pay = SolanaPay("test_endpoint", "5KHw2RWVKxqCxqvzT6aj8AHNV9VDyPn9KCwLLzG89BJV")

    @patch('solana_pay.Client')
    def test_get_balance(self, mock_client):
        mock_client.return_value.get_balance.return_value = {
            "result": {"value": 1000000}
        }
        
        balance = self.solana_pay.get_balance()
        self.assertEqual(balance["result"]["value"], 1000000)

    @patch('solana_pay.Client')
    def test_send_payment(self, mock_client):
        mock_client.return_value.send_transaction.return_value = {
            "result": "success",
            "signature": "test_signature"
        }
        
        result = self.solana_pay.send_payment("recipient", 100)
        self.assertEqual(result["result"], "success")
        self.assertEqual(result["signature"], "test_signature")

if __name__ == '__main__':
    unittest.main()
