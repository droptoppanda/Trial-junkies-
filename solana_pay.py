import logging
from solana.rpc.api import Client
from solders.transaction import Transaction 
from solders.system_program import TransferParams, transfer
from solders.pubkey import Pubkey as PublicKey
from solders.keypair import Keypair
import base58

class SolanaPay:
    def __init__(self, endpoint, keypair_base58):
        self.client = Client(endpoint)
        try:
            if not keypair_base58:
                raise ValueError("Keypair cannot be empty")
                
            if isinstance(keypair_base58, str):
                # Ensure the string is valid base58
                decoded = base58.b58decode(keypair_base58)
                if len(decoded) != 64:  # Expected length for ed25519 keypair
                    self.keypair = Keypair.from_base58_string(keypair_base58)
                else:
                    self.keypair = Keypair.from_bytes(decoded[:32])
            else:
                # Handle byte input
                if len(keypair_base58) != 32:
                    raise ValueError("Keypair bytes must be 32 bytes long")
                self.keypair = Keypair.from_bytes(keypair_base58)
                
        except Exception as e:
            logging.error(f"Failed to initialize keypair: {str(e)}")
            raise ValueError(f"Invalid keypair format: {str(e)}")

    def get_balance(self):
        return self.client.get_balance(self.keypair.public_key)

    def process_payment(self, amount):
        try:
            balance = self.get_balance()
            balance_value = balance.get('result', {}).get('value', 0)
            
            if balance_value < amount:
                return False, "Insufficient balance"
                
            if amount <= 0:
                return False, "Invalid payment amount"
                
            # Create and send transaction
            recipient = self.keypair.public_key
            transaction = self.create_payment(amount, recipient)
            response = self.client.send_transaction(transaction, self.keypair)
            
            if not response or 'result' not in response:
                return False, "Transaction failed"
                
            # Verify transaction
            verification = self.verify_payment(response['result'])
            if not verification:
                return False, "Payment verification failed"
                
            return True, response['result']
        except Exception as e:
            logging.error(f"Payment processing error: {str(e)}")
            return False, str(e)

    def create_payment(self, amount, recipient):
        transaction = Transaction()
        transfer_params = TransferParams(
            from_pubkey=self.keypair.public_key,
            to_pubkey=PublicKey(recipient),
            lamports=amount
        )
        transaction.add(transfer(transfer_params))
        return transaction

    def verify_payment(self, transaction_id):
        response = self.client.get_confirmed_transaction(transaction_id)
        return response

    def receive_subscription(self, amount, sender):
        transaction = self.create_payment(amount, self.keypair.public_key)        
        response = self.client.send_transaction(transaction, self.keypair)        
        return response

    def receive_funds(self, amount, sender):
        transaction = self.create_payment(amount, self.keypair.public_key)        
        response = self.client.send_transaction(transaction, self.keypair)        
        return response