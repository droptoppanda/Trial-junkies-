
import unittest
from unittest.mock import patch, MagicMock
from solana_pay import SolanaPay

class TestSolanaPay(unittest.TestCase):
    def setUp(self):
        # Using a consistent test keypair
        test_keypair = "[247,241,180,137,132,142,50,226,49,251,34,166,153,159,12,3,241,127,85,12,131,157,249,245,218,172,189,68,218,99,141,183,150,97,163,185,91,235,137,183,19,188,10,135,74,218,136,191,188,87,194,143,242,178,197,160,122,249,103,64,92,216,219,235]"
        self.solana_pay = SolanaPay("test_endpoint", test_keypair)

    @patch('solana_pay.Client')
    def test_get_balance(self, mock_client):
        # Configure the mock client instance
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_balance.return_value = {
            "result": {"value": 1000000}
        }
        
        # Replace the test instance's client with our mock
        self.solana_pay.client = mock_client_instance
        
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
        mock_client.return_value.get_confirmed_transaction.return_value = {
            "result": {"confirmations": 1}
        }
        
        success, result = self.solana_pay.process_payment(100)
        self.assertTrue(success)
        self.assertEqual(result, "test_signature")

if __name__ == '__main__':
    unittest.main()
