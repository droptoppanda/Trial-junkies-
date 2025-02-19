import unittest
from unittest.mock import patch
from form_filler_scraper_agent import FormFillerScraperAgent

class TestFormFillerScraperAgent(unittest.TestCase):
    def setUp(self):
        self.agent = FormFillerScraperAgent(platform_url="http://example.com", webdriver_path="/path/to/chromedriver")

    @patch('form_filler_scraper_agent.requests.post')
    def test_scrape_form_fields(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"form_fields": {"name": "John Doe"}}
        form_fields = self.agent.scrape_form_fields("http://example.com")
        self.assertEqual(form_fields["name"], "John Doe")

if __name__ == '__main__':
    unittest.main()
