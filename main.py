
import logging
import os
import subprocess
from dotenv import load_dotenv

# Set up logging first
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def install_dependencies():
    packages = [
        'asyncio', 'base58', 'discord-py', 'google-generativeai',
        'python-dotenv', 'rapid-api-client', 'requests', 'selenium',
        'solana', 'solders', 'web3', 'webdriver-manager'
    ]
    
    try:
        package_list = ' '.join(packages)
        subprocess.run(['upm', 'add'] + packages, check=True)
        logging.info("Successfully installed all packages")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install packages: {e}")
        raise

# Install dependencies before imports
install_dependencies()

# Now import the rest
from trial_request_agent import TrialRequestAgent
from credential_generation_agent import CredentialGenerationAgent
from profile_generation_agent import ProfileGenerationAgent
from trial_execution_agent import TrialExecutionAgent
from form_filler_scraper_agent import FormFillerScraperAgent
from verification_agent import VerificationAgent
from proxy_agent import ProxyAgent
from solana_pay import SolanaPay

load_dotenv()

def install_dependencies():
    import subprocess
    logging.info("Installing dependencies...")
    try:
        subprocess.run(['upm', 'add', 'requests', 'discord-py', 'google-generativeai', 'python-dotenv', 'selenium', 'solana'], check=True)
        logging.info("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install dependencies: {e}")
        raise

def main():
    logging.basicConfig(level=logging.INFO)
    try:
        from discord_bot import run_bot
        run_bot()
    except Exception as e:
        logging.error(f"Error starting bot: {e}")
        raise
    
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
        phone = credential_generation_agent.generate_phone()
        card = credential_generation_agent.generate_card()

        # Generate profile
        profile = profile_generation_agent.generate_profile()
        profile.update({
            'email': email,
            'phone': phone,
            'card': card
        })

        # Validate configuration
        required_env_vars = {
            'SOLANA_ENDPOINT': os.getenv('SOLANA_ENDPOINT'),
            'WALLET_KEYPAIR': os.getenv('WALLET_KEYPAIR'),
            'WEBDRIVER_PATH': os.getenv('WEBDRIVER_PATH'),
            'API_KEY_SUBSCRIPTION': os.getenv('API_KEY_SUBSCRIPTION')
        }
        
        missing_vars = [k for k, v in required_env_vars.items() if not v]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
        # Initialize payment system
        try:
            solana_pay = SolanaPay(required_env_vars['SOLANA_ENDPOINT'], 
                                 required_env_vars['WALLET_KEYPAIR'])
            balance = solana_pay.get_balance()
            if not balance or not balance.get('result', {}).get('value', 0):
                raise ValueError("Unable to verify wallet balance")
        except Exception as e:
            raise ValueError(f"Payment system initialization failed: {str(e)}")
            
        # Initialize Solana Pay
        solana_pay = SolanaPay(wallet_endpoint, wallet_keypair)
        
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
