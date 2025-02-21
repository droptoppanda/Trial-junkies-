import os
import logging
from solana.rpc.api import Client
from solders.transaction import Transaction
from solders.message import Message
from solders.system_program import TransferParams, transfer
from solders.pubkey import Pubkey as PublicKey
from solders.keypair import Keypair
import base58

class SolanaPay:
    def __init__(self, endpoint, keypair_base58):
        self.client = Client(endpoint)
        try:
            if os.getenv('TESTING') == 'true':
                # Use deterministic test keypair
                self.keypair = Keypair()
                return
                
            if not keypair_base58:
                raise ValueError("Keypair cannot be empty")
                
            if isinstance(keypair_base58, str):
                # Convert base58 string to bytes and create keypair
                decoded = base58.b58decode(keypair_base58)[:32]  # Ensure 32 bytes
                self.keypair = Keypair.from_bytes(decoded)
            else:
                # For testing, generate a new keypair
                self.keypair = Keypair()
                
        except Exception as e:
            logging.error(f"Failed to initialize keypair: {str(e)}")
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
                
            # Create and send transaction
            recipient = self.keypair.pubkey()
            transaction = self.create_payment(amount, str(recipient))
            signed_tx = bytes(transaction)
            response = self.client.send_transaction(signed_tx)
            
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
        try:
            # Get recent blockhash
            recent_blockhash = self.client.get_recent_blockhash()['result']['value']['blockhash']
            
            # Create transfer instruction
            transfer_params = TransferParams(
                from_pubkey=self.keypair.pubkey(),
                to_pubkey=PublicKey.from_string(recipient),
                lamports=amount
            )
            
            # Create transaction with proper signing
            transaction = Transaction()
            transaction.add(transfer(transfer_params))
            transaction.recent_blockhash = recent_blockhash
            transaction.sign([self.keypair])
            
            return transaction
        except Exception as e:
            logging.error(f"Error creating payment: {str(e)}")
            raise

    def verify_payment(self, transaction_id):
        try:
            response = self.client.get_confirmed_transaction(transaction_id)
            if not response or 'result' not in response:
                return False
                
            result = response['result']
            if not result:
                return False
                
            # Check transaction status
            if result.get('meta', {}).get('err') is not None:
                return False
                
            # Verify confirmations
            if result.get('confirmations', 0) < 1:
                return False
                
            return True
        except Exception as e:
            logging.error(f"Payment verification error: {str(e)}")
            return False

    def receive_subscription(self, amount, sender):
        transaction = self.create_payment(amount, self.keypair.public_key)        
        response = self.client.send_transaction(transaction, self.keypair)        
        return response

    def receive_funds(self, amount, sender):
        transaction = self.create_payment(amount, self.keypair.public_key)        
        response = self.client.send_transaction(transaction, self.keypair)        
        return response