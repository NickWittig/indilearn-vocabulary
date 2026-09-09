import math

from irt_model import IRTModel


class IRTModel_2PL(IRTModel):
    def probability_of_correct_response(self, user_skill, item_difficulty, item_discrimination):
        """
        Compute the probability of a correct response in the 2PL IRT model.

        :param user_skill: The ability level of the user (theta).
        :param item_difficulty: The difficulty level of the item (b).
        :param item_discrimination: The discrimination parameter of the item (a).
        :return: The probability of a correct response.
        """
        exponent = item_discrimination * (user_skill - item_difficulty)
        probability = 1 / (1 + math.exp(-exponent))
        return probability
