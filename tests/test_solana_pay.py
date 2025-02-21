
import unittest
from unittest.mock import patch, MagicMock
from solana_pay import SolanaPay

class TestSolanaPay(unittest.TestCase):
    def setUp(self):
        # Using valid 64-byte test keypair
        self.solana_pay = SolanaPay("test_endpoint", "4uQeVj5tqViQh7yWWGStvkEG1Zmhx6uasJtWCJziofM95zVnZh3YXhJNa1jHYdq4PmkhF9g4sfJgpDwKZ5d9u8X8")

    @patch('solana_pay.Client')
    def test_get_balance(self, mock_client):
        mock_client.return_value.get_balance.return_value = {
            "result": {"value": 1000000}
        }
        
        balance = self.solana_pay.get_balance()
        self.assertEqual(balance["result"]["value"], 1000000)

    @patch('solana_pay.Client')
    def test_process_payment(self, mock_client):
        mock_client.return_value.get_balance.return_value = {
            "result": {"value": 1000000}
        }
        mock_client.return_value.send_transaction.return_value = {
            "result": "test_signature"
        }
        
        success, result = self.solana_pay.process_payment(100)
        self.assertTrue(success)
        self.assertEqual(result, "test_signature")

if __name__ == '__main__':
    unittest.main()
