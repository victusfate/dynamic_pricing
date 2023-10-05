class DynamicPricing:
    def __init__(self, base_price, sensitivity):
        """
        :param base_price: Initial price of the item
        :param sensitivity: Sensitivity of price to changes in demand. 
                            Positive value: Price increases with increased demand. 
                            Negative value: Price decreases with increased demand.
        """
        self.base_price = base_price
        self.sensitivity = sensitivity
        self.current_demand = 0

    def record_purchase(self):
        """
        Records a purchase and adjusts the demand.
        """
        self.current_demand += 1

    def record_no_purchase(self):
        """
        Records a lack of purchase and adjusts the demand.
        """
        self.current_demand -= 1
        if self.current_demand < 0:
            self.current_demand = 0

    def get_price(self):
        """
        Calculates price based on current demand and sensitivity.
        :return: Current price
        """
        return self.base_price + self.sensitivity * self.current_demand

# Example
pricing = DynamicPricing(base_price=100, sensitivity=5)

# Simulate a sequence of events
events = ["purchase", "purchase", "no_purchase", "purchase", "no_purchase", "no_purchase"]

for event in events:
    if event == "purchase":
        pricing.record_purchase()
    else:
        pricing.record_no_purchase()

    print(f"Event: {event}. Current Price: ${pricing.get_price()}")
