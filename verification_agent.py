
import requests

class VerificationAgent:
    def verify_email(self, email):
        response = requests.post("https://api.verifier.com/email", json={"email": email})
        return response.json()

    def verify_phone(self, phone):
        response = requests.post("https://api.verifier.com/phone", json={"phone": phone})
        return response.json()

    def verify_trial_creation(self, profile):
        print(f"Verifying trial creation for {profile['name']}")
        if not profile.get('trial_created'):
            raise ValueError(f"Trial creation failed for {profile['name']}")
        print(f"Trial successfully created for {profile['name']}")

    def perform_kyc(self, user_id):
        # Logic to perform KYC verification
        pass
