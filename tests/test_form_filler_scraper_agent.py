
import unittest
from unittest.mock import patch, MagicMock
from form_filler_scraper_agent import FormFillerScraperAgent

class TestFormFillerScraperAgent(unittest.TestCase):
    def setUp(self):
        self.agent = FormFillerScraperAgent(platform_url="http://example.com")

    @patch('form_filler_scraper_agent.webdriver.Chrome')
    @patch('form_filler_scraper_agent.WebDriverWait')
    def test_scrape_form_fields(self, mock_wait, mock_chrome):
        # Setup mock driver and elements
        mock_driver = MagicMock()
        mock_form = MagicMock()
        mock_input = MagicMock()
        
        mock_input.get_attribute.side_effect = lambda attr: "text" if attr == "type" else "name" if attr == "name" else None
        mock_form.find_elements.return_value = [mock_input]
        mock_driver.find_element.return_value = mock_form
        mock_wait.return_value.until.return_value = mock_form
        mock_chrome.return_value = mock_driver
        mock_driver.quit.side_effect = None
        
        form_fields = self.agent.scrape_form_fields("http://example.com")
        self.assertIsNotNone(form_fields)
        self.assertEqual(form_fields["name"], "text")

if __name__ == '__main__':
    unittest.main()
