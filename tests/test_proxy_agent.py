
import unittest
from unittest.mock import patch, MagicMock
from proxy_agent import ProxyAgent

class TestProxyAgent(unittest.TestCase):
    def setUp(self):
        os.environ['PROXY_API_KEY'] = 'test_key'
        self.agent = ProxyAgent()

    @patch('proxy_agent.requests.get')
    def test_get_new_proxy(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "proxy": {
                "ip": "192.168.1.1",
                "port": "8080",
                "country": "US"
            }
        }
        
        proxy = self.agent.get_new_proxy()
        self.assertEqual(proxy["ip"], "192.168.1.1")
        self.assertEqual(proxy["port"], "8080")
        self.assertEqual(proxy["country"], "US")

if __name__ == '__main__':
    unittest.main()
