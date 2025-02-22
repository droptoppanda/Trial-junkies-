import os
import unittest
from unittest.mock import patch, MagicMock
from solana_pay import SolanaPay

class TestSolanaPay(unittest.TestCase):
    def setUp(self):
        self.test_endpoint = "https://api.devnet.solana.com"
        self.test_keypair = "4NMwxzFrpZQVX9sXZwSvSD8CX6WdZheQh7hXCFAEYQm"
        self.solana_pay = SolanaPay(self.test_endpoint, self.test_keypair)

    @patch('solana_pay.Client')
    def test_get_balance(self, mock_client):
        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.value = 1000000
        mock_instance.get_balance.return_value = mock_response
        mock_client.return_value = mock_instance
        self.solana_pay.client = mock_instance  # Set the mocked client directly

        balance = self.solana_pay.get_balance()
        self.assertEqual(balance.value, 1000000)

    @patch('solana_pay.Client')
    def test_process_payment(self, mock_client):
        mock_instance = MagicMock()
        
        # Mock balance check
        mock_balance = MagicMock()
        mock_balance.value = 1000000
        mock_instance.get_balance.return_value = mock_balance

        # Mock blockhash
        mock_blockhash = MagicMock()
        mock_blockhash.value = MagicMock()
        mock_blockhash.value.blockhash = "11111111111111111111111111111111"
        mock_instance.get_latest_blockhash.return_value = mock_blockhash

        # Mock send_transaction response
        mock_tx = MagicMock()
        mock_tx.value = "test_signature"
        mock_instance.send_transaction = MagicMock(return_value=mock_tx)

        # Mock confirmation check
        mock_confirm = MagicMock()
        mock_confirm.value = {
            "meta": {"err": None},
            "transaction": {"signatures": ["test_signature"]},
            "confirmations": 1
        }
        mock_instance.get_confirmed_transaction.return_value = mock_confirm

        os.environ['TESTING'] = 'true'
        
        mock_client.return_value = mock_instance
        self.solana_pay.client = mock_instance  # Set the mocked client directly

        success, result = self.solana_pay.process_payment(100)
        self.assertTrue(success)
        self.assertEqual(result, "test_signature")

if __name__ == '__main__':
    unittest.main()