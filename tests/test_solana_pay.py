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
        mock_response = MagicMock()
        mock_response.value = 1000000
        mock_client.return_value.get_balance.return_value = mock_response

        balance = self.solana_pay.get_balance()
        self.assertEqual(balance.value, 1000000)

    @patch('solana_pay.Client')
    def test_process_payment(self, mock_client):
        # Mock balance check
        mock_balance = MagicMock()
        mock_balance.value = 1000000
        mock_client.return_value.get_balance.return_value = mock_balance

        # Mock blockhash
        mock_blockhash = MagicMock()
        mock_blockhash.value.blockhash = bytes([0] * 32)
        mock_client.return_value.get_latest_blockhash.return_value = mock_blockhash

        # Mock transaction
        mock_tx = MagicMock()
        mock_tx.value = "test_signature"
        mock_client.return_value.send_transaction.return_value = mock_tx

        # Mock confirmation
        mock_confirm = MagicMock()
        mock_confirm.value = {
            "meta": {"err": None},
            "transaction": {"signatures": ["test_signature"]},
            "confirmations": 1
        }
        mock_client.return_value.get_confirmed_transaction.return_value = mock_confirm

        success, result = self.solana_pay.process_payment(100)
        self.assertTrue(success)
        self.assertEqual(result, "test_signature")

if __name__ == '__main__':
    unittest.main()