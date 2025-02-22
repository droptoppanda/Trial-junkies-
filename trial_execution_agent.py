import logging
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import shutil
import stat
from verification_agent import VerificationAgent

class TrialExecutionAgent:
    def __init__(self, platform_url, webdriver_path=None):
        self.platform_url = platform_url
        self.webdriver_path = webdriver_path
        self.setup_chrome_driver()

    def setup_chrome_driver(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver_path = ChromeDriverManager().install()

        # Ensure executable permissions
        st = os.stat(driver_path)
        os.chmod(driver_path, st.st_mode | stat.S_IEXEC)

        self.webdriver_path = driver_path
        self.chrome_options = chrome_options

    def execute_trial(self, profile, form_fields, discord_user_id=None, payment_required=False):
        driver = None
        try:
            # Validate inputs
            if not profile or not isinstance(profile, dict):
                raise ValueError("Invalid profile data")

            # Verify subscription if discord_user_id is provided
            if discord_user_id:
                from subscription_verification import verify_subscription
                is_active, is_trial, sub_details = verify_subscription(discord_user_id)
                if not is_active:
                    raise ValueError("Active subscription required for trial creation")
                if sub_details.get('trials_remaining', 0) <= 0:
                    raise ValueError("No trials remaining in current subscription")

            # Verify payment if required
            if payment_required:
                from solana_pay import SolanaPay
                import os

                solana_pay = SolanaPay(
                    os.getenv('SOLANA_ENDPOINT'),
                    os.getenv('WALLET_KEYPAIR')
                )

                payment_status, message = solana_pay.process_payment(float(os.getenv('TRIAL_PAYMENT_AMOUNT', '0.1')))
                if not payment_status:
                    raise ValueError(f"Payment verification failed: {message}")

            # Verify trial eligibility
            from verification_agent import VerificationAgent
            verification_agent = VerificationAgent()
            verification_agent.verify_trial_creation(profile)
            if not form_fields or not isinstance(form_fields, dict):
                raise ValueError("Invalid form fields")

            logging.info(f"Executing trial signup for {profile.get('name', 'Unknown')}")

            # Initialize WebDriver with retry logic
            for attempt in range(3):
                try:
                    driver = webdriver.Chrome(
                        service=Service(self.webdriver_path),
                        options=self.chrome_options
                    )
                    driver.get(self.platform_url)
                    break
                except Exception as e:
                    if attempt == 2:
                        raise
                    logging.warning(f"WebDriver initialization attempt {attempt + 1} failed: {e}")
                    time.sleep(2)

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

            trial_details = {
                "status": "success",
                "profile": profile,
                "credentials": form_fields,
                "platform_url": self.platform_url,
                "timestamp": datetime.datetime.now().isoformat()
            }
            return trial_details

        except Exception as e:
            logging.error(f"Selenium Error: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }

        finally:
            if driver:
                driver.quit()