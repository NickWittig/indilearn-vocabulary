import numpy as np
from scipy.stats import norm


class ItemResponseTheory:
    """
    Manages exercises and users, updating their difficulty and skill levels based on user responses.
    """

    def __init__(self):
        self.gamma_values = [0, 0.5, 1]
        self.learning_rate = 0.01
        self.item_discrimination_std = 0.1
        self.item_difficulty_std = 0.5
        self.user_ability_std = 0

    # Predict probability of solving an item using the 2PL model
    def get_probability_of_correct_response(self, user, item) -> float:
        exponent = item.discrimination * (user.ability - item.difficulty)
        probability = 1 / (1 + np.exp(-exponent))
        return probability

    def update_user_skill(self, user, item, user_item) -> None:
        users, items = self.process_solved_items([user], [item], [user_item])
        return users, items

    # Helper function to ensure scalar inputs
    def _to_scalar(self, value):
        """Convert array-like values with only one element to a scalar."""
        if isinstance(value, np.ndarray) and value.size == 1:
            return value.item()  # Convert single-element array to scalar
        return value

    # Compute Delta
    def __compute_delta(self, value1, value2, std_dev, response):
        # Ensure scalar inputs
        value1 = self._to_scalar(value1)
        value2 = self._to_scalar(value2)
        std_dev = self._to_scalar(std_dev)

        if response == 0:
            delta = (-(value2 / std_dev) * norm.pdf(value2 / std_dev)) / (
                norm.cdf(value1 / std_dev) - norm.cdf(value2 / std_dev)
            ) + (
                (norm.pdf(value1 / std_dev) - norm.pdf(value2 / std_dev))
                / (norm.cdf(value1 / std_dev) - norm.cdf(value2 / std_dev))
            ) ** 2
            return delta
        elif response == 1:
            delta = ((value1 / std_dev) * norm.pdf(value1 / std_dev)) / (
                norm.cdf(value1 / std_dev) - norm.cdf(value2 / std_dev)
            ) + (
                (norm.pdf(value1 / std_dev) - norm.pdf(value2 / std_dev))
                / (norm.cdf(value1 / std_dev) - norm.cdf(value2 / std_dev))
            ) ** 2
            return delta
        else:
            return 0

    # Update item and ability parameters and their standard deviations
    def __update_parameters(self, item, user, response, gamma_values):
        combined_std_dev = np.sqrt(
            1
            + self.item_discrimination_std**2
            + (self.item_difficulty_std * user.ability) ** 2
            + (self.user_ability_std * item.difficulty) ** 2
        )
        arg1 = item.discrimination + item.difficulty * user.ability - gamma_values[response]
        arg2 = item.discrimination + item.difficulty * user.ability - gamma_values[response + 1]

        delta_temp = self.__compute_delta(arg1, arg2, combined_std_dev, response)

        delta_discrimination = (self.item_discrimination_std / combined_std_dev) ** 2 * delta_temp
        delta_difficulty = (self.item_difficulty_std * user.ability / combined_std_dev) ** 2 * delta_temp
        delta_ability = (self.user_ability_std * item.difficulty / combined_std_dev) ** 2 * delta_temp

        return delta_discrimination, delta_difficulty, delta_ability

    def update_std_values(self, items, users):
        self.item_discrimination_std = float(np.std([item.discrimination for item in items]))
        self.item_difficulty_std = float(np.std([item.difficulty for item in items]))
        self.user_ability_std = float(np.std([user.ability for user in users]))

    # Function to update user and item parameters based on solved items
    def process_solved_items(self, users, items, solved_items):

        updated_users = []
        updated_items = []

        for solved_item in solved_items:
            user = next(user for user in users if user.id == solved_item.user_id)
            item = next(item for item in items if item.id == solved_item.item_id)
            response = solved_item.correctness

            # Update parameters
            delta_discrimination, delta_difficulty, delta_ability = self.__update_parameters(
                item, user, response, self.gamma_values
            )

            # Update user's ability and item's parameters
            user.ability += float(delta_ability * self.learning_rate)
            item.difficulty += float(delta_difficulty * self.learning_rate)
            item.discrimination += float(delta_discrimination * self.learning_rate)

            updated_users.append(user)
            updated_items.append(item)
        return updated_users, updated_items
