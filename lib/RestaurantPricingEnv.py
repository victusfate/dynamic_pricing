import numpy as np
import gym
from gym import spaces

class RestaurantPricingEnv(gym.Env):
    def __init__(self, capacity=100, base_demand=5):
        super(RestaurantPricingEnv, self).__init__()

        # Define the action space (10 discrete price levels)
        self.action_space = spaces.Discrete(10)

        # Define the observation space: [current_bookings, week_of_year, day_of_week, time_of_day]
        self.observation_space = spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32)

        # Base parameters
        self.min_spend = 10
        self.capacity = capacity
        self.base_demand = base_demand

    def reset(self):
        """Reset the environment to its initial state."""
        initial_state = [
            0,  # current_bookings
            np.random.randint(1, 53),  # week_of_year
            np.random.randint(1, 8),   # day_of_week
            np.random.randint(0, 24)   # time_of_day
        ]
        self.state = np.array(initial_state)
        return self.state

    def step(self, action):
        """Take an action (set a price level) and return the new state, reward, done, and additional info."""
        state = self.state

        price_level = self.min_spend + action

        base_bookings = self.base_demand

        # Modify demand based on price level
        if price_level <= self.min_spend + 3:
            base_bookings += np.random.randint(1, 4)
        elif price_level <= self.min_spend + 6:
            base_bookings += np.random.randint(-2, 2)
        else:
            base_bookings -= np.random.randint(1, 4)

        if state[2] in [4, 5, 6] and 18 <= state[3] <= 23:  # Check if it's one of those days and it's evening (6 PM - 11 PM)
            if state[2] == 5:  # Friday
                base_bookings += np.random.randint(3, 7)
            elif state[2] == 6:  # Saturday
                base_bookings += np.random.randint(4, 8)
            else:  # Thursday
                base_bookings += np.random.randint(2, 6)
                state[0] += base_bookings
        
        reward = base_bookings * price_level
        state[0] += base_bookings

        # Update time logic (this example increments by hour and adjusts days/weeks accordingly)
        state[3] += 1  # Hourly timestep
        if state[3] >= 24:
            state[3] = 0
            state[2] += 1
            if state[2] > 7:
                state[2] = 1
                state[1] += 1
                if state[1] > 52:
                    state[1] = 1

        self.state = state
        done = state[0] >= self.capacity

        return np.array(state), reward, done, {}

    def render(self, mode='human'):
        """Render the environment (not implemented for this example)."""
        pass

    def close(self):
        """Close the environment (not implemented for this example)."""
        pass
