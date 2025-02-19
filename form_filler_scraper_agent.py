import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

from selenium import webdriver

class FormFillerScraperAgent:
    def __init__(self, platform_url=None, webdriver_path=None):
        self.platform_url = platform_url
        self.webdriver_path = webdriver_path
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Failed to initialize webdriver: {str(e)}")
            self.driver = None

    def setup_driver(self):
        #This function is now redundant since driver is initialized in __init__
        return self.driver

    def scrape_form_fields(self, url):
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            form = self.driver.find_element(By.TAG_NAME, "form")
            fields = form.find_elements(By.TAG_NAME, "input")

            form_data = {}
            for field in fields:
                field_type = field.get_attribute("type")
                field_name = field.get_attribute("name")
                if field_type not in ["submit", "button"] and field_name:
                    form_data[field_name] = field_type

            return form_data
        except Exception as e:
            print(f"Error scraping form: {str(e)}")
            return None
        finally:
            if self.driver:
                self.driver.quit()

    def fill_form(self, url, form_data):
        try:
            self.driver.get(url)
            for field_name, value in form_data.items():
                try:
                    field = self.driver.find_element(By.NAME, field_name)
                    field.send_keys(value)
                except:
                    continue

            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()

            return True
        except Exception as e:
            print(f"Error filling form: {str(e)}")
            return False
        finally:
            if self.driver:
                self.driver.quit()