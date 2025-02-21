
import os
import pytest

@pytest.fixture(autouse=True)
def setup_test_env():
    """Setup test environment variables"""
    os.environ['TESTING'] = 'true'
    os.environ['RAPIDAPI_KEY'] = 'test_key'
    os.environ['SOLANA_ENDPOINT'] = 'test_endpoint'
    os.environ['DISCORD_BOT_TOKEN'] = 'test_token'
    os.environ['GEMINI_API_KEY'] = 'test_key'
