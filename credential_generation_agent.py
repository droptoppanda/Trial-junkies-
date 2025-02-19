
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CredentialGenerationAgent:
    def __init__(self):
        self.personator_api_key = os.getenv('PERSONATOR_API_KEY')
        self.virtual_number_api_key = os.getenv('VIRTUAL_NUMBER_API_KEY')
        self.card_api_key = os.getenv('FAKE_VALID_CC_DATA_GENERATOR_API_KEY')
        
    def generate_email(self):
        url = "https://api.namefake.com/english-united-states/random"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("email")
        return None

    def generate_phone(self):
        url = "https://virtual-number.p.rapidapi.com/api/v1/e-sim/country-numbers"
        headers = {
            "X-RapidAPI-Key": self.virtual_number_api_key,
            "X-RapidAPI-Host": "virtual-number.p.rapidapi.com"
        }
        params = {"countryId": "1"}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("number")
        return None

    def generate_card(self):
        url = "https://fake-valid-cc-data-generator.p.rapidapi.com/card"
        headers = {
            "X-RapidAPI-Key": self.card_api_key,
            "X-RapidAPI-Host": "fake-valid-cc-data-generator.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
