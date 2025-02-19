
import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

class ProxyAgent:
    def __init__(self):
        self.api_key = os.getenv('PROXY_API_KEY')
        if not self.api_key:
            raise ValueError("PROXY_API_KEY not found in environment variables")
        
    def route_request(self, request):
        try:
            proxy_url = f"https://proxy.api/route?key={self.api_key}"
            response = requests.post(proxy_url, json=request, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Proxy routing error: {str(e)}")
            return None

    def get_new_proxy(self):
        try:
            response = requests.get(f"https://proxy.api/new?key={self.api_key}")
            response.raise_for_status()
            return response.json()['proxy']
        except Exception as e:
            logging.error(f"Error getting new proxy: {str(e)}")
            return None
