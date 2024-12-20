import numpy as np

class ACJ:
    def __init__(self, items):
        # Initialize items with equal quality parameters
        self.items = {item: 0.0 for item in items}
        self.comparisons = []  # Store all comparisons (item_a, item_b, winner)

    def select_pair(self):
        """Select the next pair for comparison."""
        if len(self.comparisons) < len(self.items):
            # Random pair selection for the first round
            return np.random.choice(list(self.items.keys()), 2, replace=False)
        else:
            # Adaptive pair selection based on quality parameters
            items = list(self.items.items())
            items.sort(key=lambda x: x[1])  # Sort by quality
            return items[0][0], items[1][0]  # Select closest pair

    def update_parameters(self):
        """Update quality parameters using Rasch model."""
        for item_a, item_b, winner in self.comparisons:
            va = self.items[item_a]
            vb = self.items[item_b]
            pa = np.exp(va - vb) / (1 + np.exp(va - vb))  # Probability A beats B

            # Update parameters
            self.items[item_a] += (1 if winner == item_a else 0 - pa)
            self.items[item_b] += (0 if winner == item_a else 1 - (1 - pa))

    def record_comparison(self, item_a, item_b, winner):
        """Store comparison results."""
        self.comparisons.append((item_a, item_b, winner))
