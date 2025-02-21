
import os
from dotenv import load_dotenv
import logging

load_dotenv()

import time
from collections import defaultdict

class RapidAPIManager:
    def __init__(self):
        self.api_key = os.getenv('RAPIDAPI_KEY')
        if not self.api_key:
            raise ValueError("RAPIDAPI_KEY not found in environment variables")
        
        self.last_request_time = defaultdict(float)
        self.request_interval = 1.0  # Minimum seconds between requests
            
        self.apis = {
            'personator': {
                'host': 'personator.p.rapidapi.com',
                'base_url': 'https://personator.p.rapidapi.com'
            },
            'temp_mail': {
                'host': 'privatix-temp-mail-v1.p.rapidapi.com',
                'base_url': 'https://privatix-temp-mail-v1.p.rapidapi.com'
            },
            'virtual_number': {
                'host': 'virtual-phone-number.p.rapidapi.com',
                'base_url': 'https://virtual-phone-number.p.rapidapi.com'
            },
            'card_generator': {
                'host': 'fake-valid-cc-data-generator.p.rapidapi.com',
                'base_url': 'https://fake-valid-cc-data-generator.p.rapidapi.com'
            },
            'scraper': {
                'host': 'scrapeninja.p.rapidapi.com',
                'base_url': 'https://scrapeninja.p.rapidapi.com'
            }
        }
    
    def get_headers(self, api_name):
        if api_name not in self.apis:
            raise ValueError(f"Unknown API: {api_name}")
            
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_request_time[api_name] < self.request_interval:
            time.sleep(self.request_interval)
        self.last_request_time[api_name] = current_time
            
        return {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': self.apis[api_name]['host']
        }
    
    def get_base_url(self, api_name):
        if api_name not in self.apis:
            raise ValueError(f"Unknown API: {api_name}")
            
        return self.apis[api_name]['base_url']
