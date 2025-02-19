
import unittest
from unittest.mock import patch, MagicMock
from verification_agent import VerificationAgent

class TestVerificationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = VerificationAgent()

    @patch('verification_agent.requests.post')
    def test_verify_email(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"verified": True}
        
        result = self.agent.verify_email("test@example.com")
        self.assertTrue(result["verified"])

    @patch('verification_agent.requests.post')
    def test_verify_phone(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"verified": True}
        
        result = self.agent.verify_phone("1234567890")
        self.assertTrue(result["verified"])

if __name__ == '__main__':
    unittest.main()
