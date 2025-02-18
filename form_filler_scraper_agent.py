import logging
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FormFillerScraperAgent:
    def __init__(self, scraping_api_key=None, webdriver_path=None):
        self.scraping_api_key = scraping_api_key or os.getenv('SCRAPING_API_KEY')
        self.webdriver_path = webdriver_path or os.getenv('WEBDRIVER_PATH')
        self.proxy_url = "https://scrapeninja.p.rapidapi.com/scrape"  # Scrape Ninja endpoint
        self.headers = {
            'x-rapidapi-key': self.scraping_api_key,
            'x-rapidapi-host': 'scrapeninja.p.rapidapi.com'
        }

    def scrape_form_fields(self, url):
        try:
            # Use Scrape Ninja to scrape the form fields
            response = requests.post(self.proxy_url, headers=self.headers, json={"url": url})
            if response.status_code == 200:
                form_fields = response.json().get("form_fields", {})
                return form_fields
            return None
        except Exception as e:
            logging.error(f"Scrape Ninja Error: {e}")
            return None

    def fill_form(self, form_fields, profile):
        # Fill form fields with profile data
        filled_form = {}
        for field, value in form_fields.items():
            filled_form[field] = profile.get(field, "")
        return filled_form
