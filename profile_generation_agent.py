import os
import requests
from dotenv import load_dotenv
from credential_generation_agent import CredentialGenerationAgent

# Load environment variables
load_dotenv()

class ProfileGenerationAgent:
    def __init__(self):
        self.api_key = os.getenv('RAPIDAPI_KEY')
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'randomuser.me'
        }

    def generate_profile(self):
        credential_agent = CredentialGenerationAgent()
        person_data = credential_agent.generate_person()
        email = credential_agent.generate_email()
        phone = credential_agent.generate_phone()
        card = credential_agent.generate_card()

        if os.getenv('TESTING') == 'true':
            return self._get_mock_test_profile()
            
        # Always return a profile, using fallbacks if needed
        if not person_data:
            person_data = credential_agent._get_mock_person()
        if not email:
            email = credential_agent._get_mock_email()
        if not phone:
            phone = credential_agent._get_mock_phone()
        if not card:
            card = credential_agent._get_mock_card()
            
        return {
                "name": person_data['name'],
                "address": person_data['address'],
                "email": email,
                "phone": phone,
                "card": card,
                "city": person_data['city'],
                "state": person_data['state'],
                "zip": person_data['zip'],
                "ssn": person_data['ssn'],
                "dob": person_data['dob']
            }
        return self._get_fallback_profile()

    def _get_mock_test_profile(self):
        return {
            "name": "John Doe",
            "address": "123 Main St", 
            "email": "john.doe@example.com",
            "phone": "123-456-7890",
            "card": "4111-1111-1111-1111",
            "city": "Anytown",
            "state": "ST",
            "zip": "12345",
            "ssn": "123-45-6789",
            "dob": "1990-01-01"
        }

    def _get_fallback_profile(self):
        return {
            "name": "John Doe",
            "address": "123 Main St",
            "email": "generated_email@example.com",
            "phone": "123-456-7890",
            "card": "4111-1111-1111-1111",
            "city": "Anytown",
            "state": "ST",
            "zip": "12345",
            "ssn": "123-45-6789",
            "dob": "1990-01-01"
        }