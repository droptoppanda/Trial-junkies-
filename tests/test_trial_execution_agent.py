import unittest
from unittest.mock import patch
from trial_execution_agent import TrialExecutionAgent

class TestTrialExecutionAgent(unittest.TestCase):
    def setUp(self):
        self.agent = TrialExecutionAgent(platform_url="http://example.com", webdriver_path="/path/to/chromedriver")

    @patch('trial_execution_agent.webdriver.Chrome')
    def test_execute_trial(self, mock_chrome):
        mock_driver = mock_chrome.return_value
        mock_driver.find_element.return_value = mock_driver
        mock_driver.find_elements.return_value = [mock_driver]
        mock_driver.get.return_value = None
        mock_driver.quit.return_value = None
        mock_driver.submit.return_value = None
        
        # Mock WebDriverWait
        mock_wait = MagicMock()
        mock_wait.until.return_value = mock_driver
        with patch('trial_execution_agent.WebDriverWait', return_value=mock_wait):

        profile = {"name": "John Doe"}
        form_fields = {"name": "John Doe"}
        result = self.agent.execute_trial(profile, form_fields)
        self.assertEqual(result["status"], "success")

if __name__ == '__main__':
    unittest.main()
