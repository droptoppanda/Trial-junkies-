import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

class FormFillerScraperAgent:
    def __init__(self, scraping_api_key, webdriver_path):
        self.scraping_api_key = scraping_api_key
        self.webdriver_path = webdriver_path

    def scrape_form_fields(self, url):
        try:
            # Initialize Selenium WebDriver (Chrome example)
            driver = webdriver.Chrome(service=Service(self.webdriver_path))
            driver.get(url)

            # Wait for the form or search results to load (adjust timeout as needed)
            WebDriverWait(driver, 10).until(
                lambda driver: driver.find_elements(By.TAG_NAME, "form") or 
                               driver.find_elements(By.ID, "search")  # Adjust search ID if necessary
            )

            # Check if it's a search page
            if driver.find_elements(By.ID, "search"):  # Adjust search ID if necessary
                search_box = driver.find_element(By.ID, "search")  # Adjust search ID if necessary
                search_term = "trial signup"  # Or any relevant term for the target platform
                search_box.send_keys(search_term)
                search_box.submit()

                # Wait for search results
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".search-result a"))  # Adjust CSS selector
                )

                # Click the first search result link
                first_result = driver.find_element(By.CSS_SELECTOR, ".search-result a")  # Adjust CSS selector
                first_result.click()

                # Now, wait for the form to load on the target page
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "form")))

            # Extract form fields
            form_fields = {}
            form = driver.find_element(By.TAG_NAME, "form")
            inputs = form.find_elements(By.TAG_NAME, "input")
            for input_element in inputs:
                name = input_element.get_attribute("name")
                if name:
                    form_fields[name] = input_element.get_attribute("value")

            driver.quit()
            return form_fields

        except Exception as e:
            logging.error(f"Selenium Error: {e}")
            return None

    def fill_form(self, form_fields, profile):
        # Fill form fields with profile data
        filled_form = {}
        for field, value in form_fields.items():
            filled_form[field] = profile.get(field, "")
        return filled_form
