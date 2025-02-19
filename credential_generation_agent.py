
import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

class CredentialGenerationAgent:
    def __init__(self):
        self.personator_api_key = os.getenv('RAPIDAPI_KEY')
        self.virtual_number_api_key = os.getenv('VIRTUAL_NUMBER_API_KEY')
        self.card_api_key = os.getenv('FAKE_VALID_CC_DATA_GENERATOR_API_KEY')
        
    def generate_person(self):
        try:
            url = "https://personator.p.rapidapi.com/generate"
            headers = {
                "X-RapidAPI-Key": self.personator_api_key,
                "X-RapidAPI-Host": "personator.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'name': f"{data.get('firstName')} {data.get('lastName')}",
                    'address': f"{data.get('streetAddress')}",
                    'city': data.get('city'),
                    'state': data.get('state'),
                    'zip': data.get('zipCode'),
                    'ssn': data.get('ssn'),
                    'dob': data.get('dateOfBirth')
                }
            logging.error(f"Personator API Error: Status {response.status_code}")
            return None
        except Exception as e:
            logging.error(f"Person generation failed: {str(e)}")
            return None
        
    def generate_email(self):
        try:
            url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/mail/id/12345/"
            headers = {
                "X-RapidAPI-Key": os.getenv('RAPIDAPI_KEY'),
                "X-RapidAPI-Host": "privatix-temp-mail-v1.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("email")
            logging.error(f"Email API Error: Status {response.status_code}")
            return None
        except Exception as e:
            logging.error(f"Email generation failed: {str(e)}")
            return None

    def generate_phone(self):
        try:
            url = "https://virtual-number.p.rapidapi.com/api/v1/e-sim/country-numbers"
            headers = {
                "X-RapidAPI-Key": self.virtual_number_api_key,
                "X-RapidAPI-Host": "virtual-number.p.rapidapi.com"
            }
            params = {"countryId": "1"}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("phone")
            logging.error(f"Phone API Error: Status {response.status_code}")
            return None
        except Exception as e:
            logging.error(f"Phone generation failed: {str(e)}")
            return None

    def generate_card(self):
        try:
            url = "https://fake-valid-cc-data-generator.p.rapidapi.com/card"
            headers = {
                "X-RapidAPI-Key": self.card_api_key,
                "X-RapidAPI-Host": "fake-valid-cc-data-generator.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json().get("card_number")
            logging.error(f"Card API Error: Status {response.status_code}")
            return None
        except Exception as e:
            logging.error(f"Card generation failed: {str(e)}")
            return None
