class SubscriptionPlan:
    def __init__(self, name, price, trial_limit):
        self.name = name
        self.price = price
        self.trial_limit = trial_limit

# Define subscription plans
FREE_TRIAL = SubscriptionPlan("Free Trial", 0.00, 1)
TEN_TRIALS = SubscriptionPlan("10 Trials", 9.99, 10)
UNLIMITED_TRIALS = SubscriptionPlan("Unlimited Trials", 45.99, float('inf'))

# List of all plans
SUBSCRIPTION_PLANS = [FREE_TRIAL, TEN_TRIALS, UNLIMITED_TRIALS]
