
import logging
import requests
from solana_pay import SolanaPay
from credential_generation_agent import CredentialGenerationAgent
from profile_generation_agent import ProfileGenerationAgent

class TrialRequestAgent:
    def __init__(self, platform):
        self.platform = platform
        self.solana_pay = SolanaPay()
        self.credential_agent = CredentialGenerationAgent()
        self.profile_agent = ProfileGenerationAgent()
        
    async def process_trial_request(self, subscription_plan):
        try:
            # Step 1: Verify payment
            success, payment_result = self.solana_pay.process_payment(subscription_plan.price)
            if not success:
                return False, f"Payment failed: {payment_result}"
                
            # Step 2: Generate credentials
            credentials = {
                'email': self.credential_agent.generate_email(),
                'phone': self.credential_agent.generate_phone(),
                'card': self.credential_agent.generate_card()
            }
            
            # Step 3: Generate profile
            profile = self.profile_agent.generate_profile()
            profile.update(credentials)
            
            return True, profile
            
        except Exception as e:
            logging.error(f"Trial request failed: {str(e)}")
            return False, str(e)
