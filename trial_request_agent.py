class TrialRequestAgent:
    def __init__(self, platform):
        self.platform = platform

    def initiate_trial_creation(self):
        print(f"Initiating trial creation for {self.platform}")
        # Orchestrate other agents