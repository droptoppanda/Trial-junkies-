import unittest
from unittest.mock import patch
from credential_generation_agent import CredentialGenerationAgent

class TestCredentialGenerationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = CredentialGenerationAgent()

    @patch('credential_generation_agent.requests.get')
    def test_generate_email(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"email": "test@example.com"}
        email = self.agent.generate_email()
        self.assertIsNotNone(email)

    @patch('credential_generation_agent.requests.get')
    def test_generate_phone(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"phoneNumber": "123-456-7890"}]
        phone = self.agent.generate_phone()
        self.assertEqual(phone, "123-456-7890")

    @patch('credential_generation_agent.requests.get')
    def test_generate_card(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"card_number": "4111-1111-1111-1111"}
        card = self.agent.generate_card()
        self.assertEqual(card, "4111-1111-1111-1111")

if __name__ == '__main__':
    unittest.main()
