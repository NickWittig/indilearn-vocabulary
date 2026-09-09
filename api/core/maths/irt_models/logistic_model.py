import math

from irt_model import IRTModel


class LogisticIRTModel(IRTModel):
    """
    Implements the logistic function to calculate the probability of a correct response.
    """

    def probability_of_correct_response(self, skill: float, difficulty: float) -> float:
        return 1 / (1 + math.exp(difficulty - skill))
