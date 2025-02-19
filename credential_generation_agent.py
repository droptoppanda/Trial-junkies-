
import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

class CredentialGenerationAgent:
    def __init__(self):
        from rapid_api_manager import RapidAPIManager
        self.api_manager = RapidAPIManager()
        
    def generate_person(self):
        try:
            url = "https://personator.p.rapidapi.com/generate"
            headers = self.api_manager.get_headers('personator')
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
            headers = self.api_manager.get_headers('virtual-number')
            params = {"countryId": "1"}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get("phoneNumber")
            logging.error(f"Phone API Error: Status {response.status_code}")
            return "123-456-7890"  # Fallback value
        except Exception as e:
            logging.error(f"Phone generation failed: {str(e)}")
            return None

    def generate_card(self):
        try:
            url = "https://fake-valid-cc-data-generator.p.rapidapi.com/card"
            headers = self.api_manager.get_headers('fake-valid-cc-data-generator')
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json().get("card_number")
            logging.error(f"Card API Error: Status {response.status_code}")
            return "4111-1111-1111-1111"  # Fallback value
        except Exception as e:
            logging.error(f"Card generation failed: {str(e)}")
            return None
