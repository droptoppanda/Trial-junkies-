import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CredentialGenerationAgent:
    def __init__(self):
        self.personator_api_key = os.getenv('PERSONATOR_API_KEY')
        self.virtual_number_api_key = os.getenv('VIRTUAL_NUMBER_API_KEY')
        self.card_api_key = os.getenv('FAKE_VALID_CC_DATA_GENERATOR_API_KEY')
        self.personator_base_url = "https://personator2.p.rapidapi.com/v3/WEB/ContactVerify/doContactVerify"
        self.virtual_number_base_url = "https://virtual-number.p.rapidapi.com/generate"
        self.card_base_url = "https://fake-valid-cc-data-generator.api/endpoint/generate"  # Replace with actual endpoint
        self.personator_headers = {
            'x-rapidapi-host': 'personator2.p.rapidapi.com',
            'x-rapidapi-key': self.personator_api_key
        }
        self.virtual_number_headers = {
            'x-rapidapi-host': 'virtual-number.p.rapidapi.com',
            'x-rapidapi-key': self.virtual_number_api_key
        }
        self.card_headers = {
            'Authorization': f'Bearer {self.card_api_key}'
        }

    def generate_email(self):
        params = {
            'format': 'json',
            'act': 'check,verify,append,move',
            'email': 'test@example.com'  # Replace with actual email if needed
        }
        response = requests.get(self.personator_base_url, headers=self.personator_headers, params=params)
        if response.status_code == 200:
            return response.json().get("Records", [{}])[0].get("EmailAddress", "generated_email@example.com")
        return "generated_email@example.com"

    def generate_phone(self):
        response = requests.get(self.virtual_number_base_url, headers=self.virtual_number_headers)
        if response.status_code == 200:
            return response.json().get("phone", "123-456-7890")
        return "123-456-7890"

    def generate_card(self):
        response = requests.get(self.card_base_url, headers=self.card_headers)
        if response.status_code == 200:
            return response.json().get("card_number", "4111-1111-1111-1111")
        return "4111-1111-1111-1111"
