import requests

# Replace with your actual subscription API key and endpoint
API_KEY_SUBSCRIPTION = "your_subscription_api_key"
SUBSCRIPTION_VERIFY_URL = "https://api.example.com/verify_subscription"

def verify_subscription(discord_user_id):
    """
    Verifies a user's subscription status based on their Discord user ID.
    Returns (is_active, is_trial, subscription_details) tuple.
    """
    url = f"{SUBSCRIPTION_VERIFY_URL}?discord_id={discord_user_id}"
    headers = {"Authorization": f"Bearer {API_KEY_SUBSCRIPTION}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        is_active = data.get("is_active", False)
        is_trial = data.get("trial", False)
        subscription_details = {
            "plan": data.get("plan", ""),
            "expiry": data.get("expiry", ""),
            "trials_remaining": data.get("trials_remaining", 0)
        }
        
        return is_active, is_trial, subscription_details
        
    except requests.Timeout:
        logging.error("Subscription verification timeout")
        return False, False, {}
    except requests.RequestException as e:
        logging.error(f"Subscription verification error: {str(e)}")
        return False, False, {}

# Example usage:
if __name__ == "__main__":
    test_discord_id = "123456789012345678"
    active, trial = verify_subscription(test_discord_id)
    print(f"Subscription active: {active}, Trial active: {trial}")
