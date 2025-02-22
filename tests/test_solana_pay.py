import os
import unittest
from unittest.mock import patch, MagicMock
from solana_pay import SolanaPay
from solders.rpc.api import Client
from solders.transaction import Transaction
from solders.keypair import Keypair
from solders.pubkey import Pubkey as PublicKey

class TestSolanaPay(unittest.TestCase):
    def setUp(self):
        os.environ['TESTING'] = 'true'
        test_keypair = "4NMwxzFrpZQVX9sXZwSvSD8CX6WdZheQh7hXCFAEYQm"
        self.solana_pay = SolanaPay("test_endpoint", test_keypair)
        del os.environ['TESTING']

    @patch('solana_pay.Client')
    def test_get_balance(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_balance.return_value = {
            "result": {"value": 1000000}
        }

        self.solana_pay.client = mock_client_instance

        balance = self.solana_pay.get_balance()
        self.assertEqual(balance["result"]["value"], 1000000)

    @patch('solana_pay.Client')
    def test_process_payment(self, mock_client):
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_balance.return_value = {
            "result": {"value": 1000000}
        }

        mock_client_instance.get_recent_blockhash.return_value = {
            "result": {"value": {"blockhash": "test_blockhash"}}
        }

        mock_client_instance.send_transaction.return_value = {
            "result": "test_signature"
        }

        mock_client_instance.get_confirmed_transaction.return_value = {
            "result": {
                "meta": {"err": None},
                "transaction": {"signatures": ["test_signature"]},
                "confirmations": 1
            }
        }

        self.solana_pay.client = mock_client_instance

        success, result = self.solana_pay.process_payment(100)
        self.assertTrue(success)
        self.assertEqual(result, "test_signature")

    def test_transaction_creation(self):
        self.client = Client("https://api.devnet.solana.com")
        self.payer = Keypair()
        self.receiver = Keypair()

        transaction = self.solana_pay.create_transaction(self.payer, self.receiver, 1000)
        self.assertIsNotNone(transaction)

if __name__ == '__main__':
    unittest.main()