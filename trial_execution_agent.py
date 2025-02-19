import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

from selenium import webdriver

class TrialExecutionAgent:
    def __init__(self, platform_url, webdriver_path):
        self.platform_url = platform_url
        self.webdriver_path = webdriver_path
        logging.basicConfig(level=logging.INFO)

    def execute_trial(self, profile, form_fields):
        driver = None
        try:
            logging.info(f"Executing trial signup for {profile['name']}")

            # Initialize Selenium WebDriver (Chrome example)
            driver = webdriver.Chrome(service=Service(self.webdriver_path))
            driver.get(self.platform_url)

            # Fill form fields
            for field, value in form_fields.items():
                try:
                    input_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, field))
                    )
                    input_element.send_keys(value)
                except Exception as e:
                    logging.error(f"Error finding or filling field '{field}': {e}")
                    raise

            # Submit the form
            form = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            form.submit()

            return "Signup successful"

        except Exception as e:
            logging.error(f"Selenium Error: {e}")
            return "Signup failed"
        
        finally:
            if driver:
                driver.quit()