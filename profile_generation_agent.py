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
            'x-rapidapi-host': 'randomuser.me'  # Actual host name
        }

    def generate_profile(self):
        credential_agent = CredentialGenerationAgent()
        person_data = credential_agent.generate_person()
        
        if person_data:
            return {
                "name": person_data['name'],
                "address": person_data['address'],
                "email": credential_agent.generate_email(),
                "phone": credential_agent.generate_phone(),
                "card": credential_agent.generate_card(),
                "city": person_data['city'],
                "state": person_data['state'],
                "zip": person_data['zip'],
                "ssn": person_data['ssn'],
                "dob": person_data['dob']
            }
        return self._get_fallback_profile()
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                result = data['results'][0]
            else:
                return self._get_fallback_profile()
            return {
                "name": f"{result['name']['first']} {result['name']['last']}",
                "address": f"{result['location']['street']['number']} {result['location']['street']['name']}",
                "email": result['email'],
                "phone": result['phone'],
                "card": result['login']['uuid']
            }
        return {
            "name": "John Doe",
            "address": "123 Main St",
            "email": "generated_email@example.com",
            "phone": "123-456-7890",
            "card": "4111-1111-1111-1111"
        }


    def _get_fallback_profile(self):
        return {
            "name": "John Doe",
            "address": "123 Main St",
            "email": "generated_email@example.com",
            "phone": "123-456-7890",
            "card": "4111-1111-1111-1111"
        }
