
import unittest
from unittest.mock import patch, MagicMock
from trial_request_agent import TrialRequestAgent

class TestTrialRequestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = TrialRequestAgent(platform="test_platform")

    @patch('trial_request_agent.requests.get')
    def test_get_trial_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "url": "https://test.com/trial",
            "duration": "30 days",
            "requirements": ["email", "phone"]
        }
        mock_get.return_value = mock_response
        
        result = self.agent.get_trial_info()
        self.assertEqual(result["url"], "https://test.com/trial")
        self.assertEqual(result["duration"], "30 days")
        self.assertIn("email", result["requirements"])

if __name__ == '__main__':
    unittest.main()
