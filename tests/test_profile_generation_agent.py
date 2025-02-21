
import os
import unittest
from unittest.mock import patch, MagicMock
from profile_generation_agent import ProfileGenerationAgent

class TestProfileGenerationAgent(unittest.TestCase):
    def setUp(self):
        os.environ['TESTING'] = 'true'
        self.agent = ProfileGenerationAgent()

    def test_generate_profile(self):
        # No need to mock CredentialGenerationAgent since TESTING=true
        profile = self.agent.generate_profile()
        
        profile = self.agent.generate_profile()
        self.assertEqual(profile["name"], "John Doe")
        self.assertEqual(profile["email"], "john.doe@example.com")
        self.assertEqual(profile["phone"], "123-456-7890")
        self.assertEqual(profile["card"], "4111-1111-1111-1111")

if __name__ == '__main__':
    unittest.main()
