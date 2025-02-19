
import logging
from credential_generation_agent import CredentialGenerationAgent

def test_apis():
    logging.basicConfig(level=logging.INFO)
    agent = CredentialGenerationAgent()
    
    # Test email generation
    logging.info("Testing email generation...")
    email = agent.generate_email()
    logging.info(f"Generated email: {email}")
    
    # Test phone generation
    logging.info("Testing phone generation...")
    phone = agent.generate_phone()
    logging.info(f"Generated phone: {phone}")
    
    # Test card generation
    logging.info("Testing card generation...")
    card = agent.generate_card()
    logging.info(f"Generated card: {card}")
    
    # Test person generation
    logging.info("Testing person generation...")
    person = agent.generate_person()
    logging.info(f"Generated person: {person}")

if __name__ == "__main__":
    test_apis()
