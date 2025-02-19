
import os
import http.client
import json
from dotenv import load_dotenv

load_dotenv()

def scrape_url(url):
    conn = http.client.HTTPSConnection("scrapeninja.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
        'x-rapidapi-host': "scrapeninja.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    
    payload = json.dumps({"url": url})
    
    try:
        conn.request("POST", "/scrape", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
    except Exception as e:
        print(f"Scraping failed: {str(e)}")
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    result = scrape_url("https://news.ycombinator.com/")
    print(result)
