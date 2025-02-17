import logging
from trial_request_agent import TrialRequestAgent
from credential_generation_agent import CredentialGenerationAgent
from profile_generation_agent import ProfileGenerationAgent
from trial_execution_agent import TrialExecutionAgent
from form_filler_scraper_agent import FormFillerScraperAgent
from verification_agent import VerificationAgent
from proxy_agent import ProxyAgent

def main():
    platform = "Platform A"
    trial_request_agent = TrialRequestAgent(platform)
    credential_generation_agent = CredentialGenerationAgent()
    profile_generation_agent = ProfileGenerationAgent()
    trial_execution_agent = TrialExecutionAgent(platform_url="https://platform-a.com/signup")
    form_filler_scraper_agent = FormFillerScraperAgent(scraping_api_key="your_scraping_api_key")
    verification_agent = VerificationAgent()
    proxy_agent = ProxyAgent()

    trial_request_agent.initiate_trial_creation()
    email = credential_generation_agent.generate_email()
    phone = credential_generation_agent.generate_phone()
    card = credential_generation_agent.generate_card()
    profile = profile_generation_agent.generate_profile()
    
    # Get URL from user
    trial_signup_url = input("Enter the trial signup URL (or search page URL): ")
    scraped_form_fields = form_filler_scraper_agent.scrape_form_fields(trial_signup_url)
    
    signup_result = trial_execution_agent.execute_trial(profile, scraped_form_fields)
    verified = verification_agent.verify_trial_creation(profile)

    if signup_result == "Signup successful" and verified:
        logging.info("Trial created successfully!")
    else:
        logging.error("Trial creation failed.")

if __name__ == "__main__":
    main()
