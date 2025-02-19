
import os
import requests
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

class ScrapingAgent:
    def __init__(self):
        self.api_key = os.getenv('RAPIDAPI_KEY')
        self.headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': "scrapeninja.p.rapidapi.com"
        }

    def scrape_url(self, url, use_proxy=True):
        try:
            payload = {
                "url": url,
                "useProxy": use_proxy,
                "returnHtml": True
            }
            
            response = requests.post(
                "https://scrapeninja.p.rapidapi.com/scrape",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Scraping failed with status {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"Scraping error: {str(e)}")
            return None

if __name__ == "__main__":
    scraper = ScrapingAgent()
    result = scraper.scrape_url("https://example.com")
    print(json.dumps(result, indent=2))
