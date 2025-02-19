import requests

# Replace with your actual subscription API key and endpoint
API_KEY_SUBSCRIPTION = "your_subscription_api_key"
SUBSCRIPTION_VERIFY_URL = "https://api.example.com/verify_subscription"

def verify_subscription(discord_user_id):
    """
    Verifies a user's subscription status based on their Discord user ID.
    Returns True if active, False otherwise.
    """
    url = f"{SUBSCRIPTION_VERIFY_URL}?discord_id={discord_user_id}"
    headers = {"Authorization": f"Bearer {API_KEY_SUBSCRIPTION}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Expecting a JSON response like { "is_active": true, "trial": true }
            return data.get("is_active", False), data.get("trial", False)
    except Exception as e:
        print(f"Error verifying subscription: {e}")
    return False, False

# Example usage:
if __name__ == "__main__":
    test_discord_id = "123456789012345678"
    active, trial = verify_subscription(test_discord_id)
    print(f"Subscription active: {active}, Trial active: {trial}")
