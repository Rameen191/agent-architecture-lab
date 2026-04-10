import random
import math
from src.agents import Environment


class TP_env(Environment):
    """Paper buying environment with stochastic price and consumption"""

    # Price delta pattern from page 4 (simplified for tutorial)
    price_delta = [
        0, 0, 0, 21, 0, 20, 0, -64, 0, 0, 23, 0, 0, 0, -35,
        0, 76, 0, -41, 0, 0, 0, 21, 0, 5, 0, 5, 0, 0, 0, 5
    ]

    sd = 5  # Noise standard deviation

    def __init__(self):
        """Initialize environment state"""
        super().__init__()
        self.time = 0
        self.stock = 20
        self.stock_history = []
        self.price_history = []
        self.price = None

    def initial_percept(self):
        """Return initial percept"""
        self.stock_history.append(self.stock)

        # Initial price around 234 with noise
        self.price = round(234 + self.sd * random.gauss(0, 1))
        self.price_history.append(self.price)

        return {'price': self.price, 'instock': self.stock}

    def select_from_dist(self, distribution):
        """Select value based on probability distribution"""
        rand_val = random.random()
        cumulative = 0

        for value, prob in distribution.items():
            cumulative += prob
            if rand_val < cumulative:
                return value

        return list(distribution.keys())[-1]

    def do(self, action):
        """Execute action and update environment"""

        # Consumption distribution
        used = self.select_from_dist({
            6: 0.1,
            5: 0.1,
            4: 0.1,
            3: 0.3,
            2: 0.2,
            1: 0.2
        })

        bought = action.get('buy', 0)

        self.stock = self.stock + bought - used
        self.stock_history.append(self.stock)

        self.time += 1

        # Update price with pattern + noise
        delta_index = self.time % len(self.price_delta)

        self.price = round(
            self.price
            + self.price_delta[delta_index]
            + self.sd * random.gauss(0, 1)
        )

        self.price_history.append(self.price)

        return {'price': self.price, 'instock': self.stock}