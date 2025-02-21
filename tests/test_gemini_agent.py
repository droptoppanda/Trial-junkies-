
import unittest
from unittest.mock import patch, MagicMock
from gemini_agent import GeminiAgent

class TestGeminiAgent(unittest.TestCase):
    def setUp(self):
        self.agent = GeminiAgent()

    @patch('gemini_agent.genai')
    def test_generate_content(self, mock_genai):
        mock_response = MagicMock()
        mock_response.text = "Generated response"
        
        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        
        response = self.agent.generate_content("Test prompt")
        self.assertEqual(response, "Generated response")

if __name__ == '__main__':
    unittest.main()
