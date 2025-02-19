
import os
import requests
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

class ScrapingAgent:
    def __init__(self):
        self.api_key = os.getenv('SCRAPENINJA_API_KEY')
        if not self.api_key:
            raise ValueError("SCRAPENINJA_API_KEY not found in environment variables")
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': "scrapeninja.p.rapidapi.com"
        }

    def scrape_url(self, url, use_proxy=True):
        try:
            payload = {
                "url": url,
                "useProxy": use_proxy,
                "returnHtml": True,
                "javascript": True
            }
            
            response = requests.post(
                "https://scrapeninja.p.rapidapi.com/scrape",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Scraping error: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return None

    def validate_response(self, response):
        if not response or 'html' not in response:
            return False
        return True
