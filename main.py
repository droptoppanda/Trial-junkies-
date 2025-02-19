
import logging
import os
from trial_request_agent import TrialRequestAgent
from credential_generation_agent import CredentialGenerationAgent
from profile_generation_agent import ProfileGenerationAgent
from trial_execution_agent import TrialExecutionAgent
from form_filler_scraper_agent import FormFillerScraperAgent
from verification_agent import VerificationAgent
from proxy_agent import ProxyAgent
from dotenv import load_dotenv

load_dotenv()

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        webdriver_path = os.getenv('WEBDRIVER_PATH')
        trial_request_agent = TrialRequestAgent(platform="default")
        credential_generation_agent = CredentialGenerationAgent()
        profile_generation_agent = ProfileGenerationAgent()
        trial_execution_agent = TrialExecutionAgent(webdriver_path=webdriver_path)
        form_filler_scraper_agent = FormFillerScraperAgent(webdriver_path=webdriver_path)
        verification_agent = VerificationAgent()
        proxy_agent = ProxyAgent()

        # Generate credentials
        email = credential_generation_agent.generate_email()
        if not email:
            raise ValueError("Failed to generate email")
            
        phone = credential_generation_agent.generate_phone()
        if not phone:
            raise ValueError("Failed to generate phone")
            
        card = credential_generation_agent.generate_card()
        if not card:
            raise ValueError("Failed to generate card")

        # Generate profile
        profile = profile_generation_agent.generate_profile()
        profile.update({
            'email': email,
            'phone': phone,
            'card': card
        })

        # Get URL and process form
        trial_signup_url = input("Enter the trial signup URL: ")
        form_fields = form_filler_scraper_agent.scrape_form_fields(trial_signup_url)
        
        if not form_fields:
            raise ValueError("Failed to scrape form fields")

        # Execute trial signup
        success = trial_execution_agent.execute_trial(profile, form_fields)
        if success:
            logging.info("Trial created successfully!")
        else:
            logging.error("Trial creation failed.")

    except Exception as e:
        logging.error(f"Error in trial creation process: {str(e)}")

if __name__ == "__main__":
    main()
