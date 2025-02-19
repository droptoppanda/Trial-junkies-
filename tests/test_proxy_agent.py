
import unittest
from unittest.mock import patch, MagicMock
from proxy_agent import ProxyAgent

class TestProxyAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ProxyAgent()

    @patch('proxy_agent.requests.get')
    def test_get_proxy(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "ip": "192.168.1.1",
            "port": "8080",
            "country": "US"
        }
        
        proxy = self.agent.get_proxy()
        self.assertEqual(proxy["ip"], "192.168.1.1")
        self.assertEqual(proxy["port"], "8080")
        self.assertEqual(proxy["country"], "US")

if __name__ == '__main__':
    unittest.main()
