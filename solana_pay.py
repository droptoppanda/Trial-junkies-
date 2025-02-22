
import os
import logging
import base58
from solana.rpc.api import Client
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solders.keypair import Keypair
from solders.pubkey import Pubkey as PublicKey

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SolanaPay:
    def __init__(self, endpoint="https://api.devnet.solana.com", keypair_base58=None):
        try:
            self.client = Client(endpoint)
            # Verify connection
            self.client.get_version()
            logger.info(f"Initialized Solana client with endpoint: {endpoint}")
        except Exception as e:
            logger.error(f"Failed to initialize Solana client: {str(e)}")
            raise RuntimeError(f"Solana client initialization failed. Please verify package compatibility: {str(e)}")
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
                self.keypair = Keypair.from_seed(decoded)
            else:
                self.keypair = Keypair()

        except Exception as e:
            logger.error(f"Failed to initialize keypair: {str(e)}")
            raise ValueError(f"Invalid keypair format: {str(e)}")

    def get_balance(self):
        return self.client.get_balance(self.keypair.pubkey)

    def process_payment(self, amount):
        try:
            balance = self.get_balance()
            balance_value = balance.get('result', {}).get('value', 0)

            if balance_value < amount:
                return False, "Insufficient balance"

            if amount <= 0:
                return False, "Invalid payment amount"

            recipient = self.keypair.pubkey
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
            recent_blockhash = self.client.get_latest_blockhash().value.blockhash
            transfer_params = TransferParams(
                from_pubkey=self.keypair.pubkey,
                to_pubkey=PublicKey(recipient),
                lamports=amount
            )
            transfer_ix = transfer(transfer_params)
            transaction = Transaction()
            transaction.add(transfer_ix)
            transaction.recent_blockhash = recent_blockhash
            transaction.sign(self.keypair)
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
            recent_blockhash = self.client.get_latest_blockhash().value.blockhash
            transfer_params = TransferParams(
                from_pubkey=payer.pubkey,
                to_pubkey=receiver.pubkey,
                lamports=amount
            )
            transfer_ix = transfer(transfer_params)
            transaction = Transaction().add(transfer_ix)
            transaction.sign([payer])
            return transaction
        except Exception as e:
            logger.error(f"Error creating transaction: {str(e)}")
            raise
