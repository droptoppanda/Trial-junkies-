import unittest
from unittest.mock import patch
from profile_generation_agent import ProfileGenerationAgent

class TestProfileGenerationAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ProfileGenerationAgent()

    @patch('profile_generation_agent.requests.get')
    def test_generate_profile(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "results": [{
                "name": {"first": "John", "last": "Doe"},
                "location": {"street": {"number": 123, "name": "Main St"}},
                "email": "john.doe@example.com",
                "phone": "123-456-7890",
                "login": {"uuid": "4111-1111-1111-1111"}
            }]
        }
        profile = self.agent.generate_profile()
        self.assertEqual(profile["name"], "John Doe")
        self.assertEqual(profile["address"], "123 Main St")
        self.assertEqual(profile["email"], "john.doe@example.com")
        self.assertEqual(profile["phone"], "123-456-7890")
        self.assertEqual(profile["card"], "4111-1111-1111-1111")

if __name__ == '__main__':
    unittest.main()
