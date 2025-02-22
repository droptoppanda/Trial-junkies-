import os
import logging
import base58
from solders.rpc.api import Client
from solders.transaction import Transaction
from solders.message import Message
from solders.system_program import TransferParams, transfer
from solders.pubkey import Pubkey as PublicKey
from solders.keypair import Keypair
from solders.hash import Hash

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SolanaPay:
    def __init__(self, endpoint="https://api.devnet.solana.com", keypair_base58=None):
        self.client = Client(endpoint)
        logger.info(f"Initialized Solana client with endpoint: {endpoint}")
        try:
            if os.getenv('TESTING') == 'true':
                self.keypair = Keypair()
                return

            if not keypair_base58:
                keypair_base58 = os.getenv('KEYPAIR')

            if not keypair_base58:
                raise ValueError("Keypair cannot be empty")

            if isinstance(keypair_base58, str):
                decoded = base58.b58decode(keypair_base58)[:32]
                self.keypair = Keypair.from_bytes(decoded)
            else:
                self.keypair = Keypair()

        except Exception as e:
            logger.error(f"Failed to initialize keypair: {str(e)}")
            raise ValueError(f"Invalid keypair format: {str(e)}")

    def get_balance(self):
        return self.client.get_balance(self.keypair.pubkey())

    def process_payment(self, amount):
        try:
            balance = self.get_balance()
            balance_value = balance.get('result', {}).get('value', 0)

            if balance_value < amount:
                return False, "Insufficient balance"

            if amount <= 0:
                return False, "Invalid payment amount"

            recipient = self.keypair.pubkey()
            transaction = self.create_payment(amount, str(recipient))
            response = self.client.send_transaction(transaction)

            if not response or 'result' not in response:
                return False, "Transaction failed"

            verification = self.verify_payment(response['result'])
            if not verification:
                return False, "Payment verification failed"

            return True, response['result']
        except Exception as e:
            logger.error(f"Payment processing error: {str(e)}")
            return False, str(e)

    def create_payment(self, amount, recipient):
        try:
            recent_blockhash = self.client.get_recent_blockhash()['result']['value']['blockhash']
            transfer_params = TransferParams(
                from_pubkey=self.keypair.pubkey(),
                to_pubkey=PublicKey.from_string(recipient),
                lamports=amount
            )
            transfer_ix = transfer(transfer_params)
            message = Message.new_with_blockhash(
                [transfer_ix],
                self.keypair.pubkey(),
                Hash.from_string(recent_blockhash)
            )
            transaction = Transaction(
                from_keypairs=[self.keypair],
                message=message,
                recent_blockhash=recent_blockhash
            )
            return transaction
        except Exception as e:
            logger.error(f"Error creating payment: {str(e)}")
            raise

    def verify_payment(self, transaction_id):
        try:
            response = self.client.get_confirmed_transaction(transaction_id)
            if not response or 'result' not in response:
                return False

            result = response['result']
            if not result:
                return False

            if result.get('meta', {}).get('err') is not None:
                return False

            if result.get('confirmations', 0) < 1:
                return False

            return True
        except Exception as e:
            logger.error(f"Payment verification error: {str(e)}")
            return False

    def create_transaction(self, payer: Keypair, receiver: Keypair, amount: float):
        try:
            recent_blockhash = self.client.get_recent_blockhash()["result"]["value"]["blockhash"]
            transaction = Transaction(
                recent_blockhash=recent_blockhash,
                fee_payer=payer.pubkey()
            )
            return transaction
        except Exception as e:
            logger.error(f"Error creating transaction: {str(e)}")
            raise