
import os
import unittest
from unittest.mock import patch, MagicMock
from gemini_agent import GeminiAgent

class TestGeminiAgent(unittest.TestCase):
    def setUp(self):
        os.environ['GEMINI_API_KEY'] = 'test_key'
        self.agent = GeminiAgent()

    @patch('gemini_agent.genai')
    def test_generate_content(self, mock_genai):
        # Test successful case
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Generated response"
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        # Configure the mock
        self.agent.model = mock_model
        
        response = self.agent.generate_content("Test prompt")
        self.assertEqual(response, "Generated response")

        # Test error case
        mock_model.generate_content.side_effect = Exception("API Error")
        error_response = self.agent.generate_content("Test prompt")
        self.assertEqual(error_response, "Error generating content: API Error")

if __name__ == '__main__':
    unittest.main()
