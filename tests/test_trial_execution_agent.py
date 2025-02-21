import unittest
from unittest.mock import patch, MagicMock
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from trial_execution_agent import TrialExecutionAgent

class TestTrialExecutionAgent(unittest.TestCase):
    def setUp(self):
        self.agent = TrialExecutionAgent(platform_url="http://example.com", webdriver_path="/path/to/chromedriver")

    @patch('trial_execution_agent.webdriver.Chrome')
    @patch('trial_execution_agent.WebDriverWait')
    def test_execute_trial(self, mock_wait, mock_chrome):
        mock_driver = mock_chrome.return_value
        mock_driver.get.return_value = None
        mock_driver.quit.return_value = None

        # Mock form elements
        mock_input = MagicMock()
        mock_input.send_keys.return_value = None
        mock_form = MagicMock()
        mock_form.submit.return_value = None

        # Configure WebDriverWait mock to return our mocked elements
        mock_wait_instance = MagicMock()
        # Set up complete mocking
        mock_wait_instance.until.side_effect = [mock_input, mock_form]
        mock_wait.return_value = mock_wait_instance

        # Mock verification agent
        with patch('verification_agent.VerificationAgent') as mock_verify:
            mock_verify.return_value.verify_trial_creation.return_value = True

            # Mock successful form submission
            mock_driver.current_url = "http://example.com/success"

            profile = {"name": "John Doe", "trial_created": True}
            form_fields = {"name": "John Doe"}

            result = self.agent.execute_trial(profile, form_fields)

            # Verify method calls
            mock_driver.get.assert_called_once_with("http://example.com")
            mock_wait_instance.until.assert_called()
            self.assertEqual(result["status"], "success")

if __name__ == '__main__':
    unittest.main()