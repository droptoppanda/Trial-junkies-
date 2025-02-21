import os
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
            if os.getenv('TESTING') == 'true':
                # Use deterministic test keypair
                self.keypair = Keypair()
                return
                
            if not keypair_base58:
                raise ValueError("Keypair cannot be empty")
                
            if isinstance(keypair_base58, str):
                # Try to create keypair directly from base58 string
                self.keypair = Keypair.from_base58_string(keypair_base58)
            else:
                # For testing, generate a new keypair if bytes are provided
                self.keypair = Keypair()
                
        except Exception as e:
            logging.error(f"Failed to initialize keypair: {str(e)}")
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
                
            # Create and send transaction
            recipient = self.keypair.pubkey
            transaction = self.create_payment(amount, str(recipient))
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
        # Get recent blockhash
        recent_blockhash = self.client.get_recent_blockhash()['result']['value']['blockhash']
        
        # Create transfer instruction
        transfer_params = TransferParams(
            from_pubkey=self.keypair.pubkey,
            to_pubkey=PublicKey(recipient),
            lamports=amount
        )
        transfer_ix = transfer(transfer_params)
        
        # Create transaction with all required parameters
        transaction = Transaction(
            from_keypairs=[self.keypair],
            message=transfer_ix,
            recent_blockhash=recent_blockhash
        )
        
        return transaction

    def verify_payment(self, transaction_id):
        response = self.client.get_confirmed_transaction(transaction_id)
        if not response or 'result' not in response:
            return False
            
        result = response['result']
        if not result:
            return False
            
        # Check if transaction was successful (no errors)
        if result.get('meta', {}).get('err') is not None:
            return False
            
        # Verify signature matches
        if not result.get('transaction', {}).get('signatures'):
            return False
            
        return True

    def receive_subscription(self, amount, sender):
        transaction = self.create_payment(amount, self.keypair.public_key)        
        response = self.client.send_transaction(transaction, self.keypair)        
        return response

    def receive_funds(self, amount, sender):
        transaction = self.create_payment(amount, self.keypair.public_key)        
        response = self.client.send_transaction(transaction, self.keypair)        
        return response