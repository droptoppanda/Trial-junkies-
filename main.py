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
    trial_execution_agent = TrialExecutionAgent()
    form_filler_scraper_agent = FormFillerScraperAgent()
    verification_agent = VerificationAgent()
    proxy_agent = ProxyAgent()

    trial_request_agent.initiate_trial_creation()
    email = credential_generation_agent.generate_email()
    phone = credential_generation_agent.generate_phone()
    card = credential_generation_agent.generate_card()
    profile = profile_generation_agent.generate_profile()
    form_fields = form_filler_scraper_agent.scrape_form_fields(platform)
    filled_form = form_filler_scraper_agent.fill_form(form_fields, profile)
    trial_execution_agent.execute_trial(profile, filled_form)
    verification_agent.verify_trial_creation(profile)

if __name__ == "__main__":
    main()
