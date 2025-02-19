
import unittest
from unittest.mock import patch, MagicMock
from profile_generation_agent import ProfileGenerationAgent

class TestProfileGenerationAgent(unittest.TestCase):
    def setUp(self):
        os.environ['TESTING'] = 'true'
        self.agent = ProfileGenerationAgent()

    @patch('credential_generation_agent.CredentialGenerationAgent')
    def test_generate_profile(self, mock_credential_agent):
        # Setup mock credential agent
        mock_instance = MagicMock()
        mock_instance.generate_person.return_value = {
            'name': 'John Doe',
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'ST',
            'zip': '12345',
            'ssn': '123-45-6789',
            'dob': '1990-01-01'
        }
        mock_instance.generate_email.return_value = "john.doe@example.com"
        mock_instance.generate_phone.return_value = "123-456-7890"
        mock_instance.generate_card.return_value = "4111-1111-1111-1111"
        
        mock_credential_agent.return_value = mock_instance
        
        profile = self.agent.generate_profile()
        self.assertEqual(profile["name"], "John Doe")
        self.assertEqual(profile["email"], "john.doe@example.com")
        self.assertEqual(profile["phone"], "123-456-7890")
        self.assertEqual(profile["card"], "4111-1111-1111-1111")

if __name__ == '__main__':
    unittest.main()
