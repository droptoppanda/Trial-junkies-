import os
import requests
from dotenv import load_dotenv

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
        url = "https://randomuser.me/api/"  # Actual endpoint
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            result = response.json()['results'][0]
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
