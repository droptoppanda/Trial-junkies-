
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

class FormFillerScraperAgent:
    def __init__(self, webdriver_path):
        self.scraping_api_key = os.getenv('SCRAPING_API_KEY')
        self.webdriver_path = webdriver_path
        
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(self.webdriver_path, options=chrome_options)

    def scrape_form_fields(self, url):
        driver = self.setup_driver()
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            form = driver.find_element(By.TAG_NAME, "form")
            fields = form.find_elements(By.TAG_NAME, "input")
            
            form_data = {}
            for field in fields:
                field_type = field.get_attribute("type")
                field_name = field.get_attribute("name")
                if field_type not in ["submit", "button"] and field_name:
                    form_data[field_name] = field_type
                    
            return form_data
        finally:
            driver.quit()

    def fill_form(self, url, form_data):
        driver = self.setup_driver()
        try:
            driver.get(url)
            for field_name, value in form_data.items():
                try:
                    field = driver.find_element(By.NAME, field_name)
                    field.send_keys(value)
                except:
                    continue
            
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            return True
        except Exception as e:
            print(f"Error filling form: {str(e)}")
            return False
        finally:
            driver.quit()
