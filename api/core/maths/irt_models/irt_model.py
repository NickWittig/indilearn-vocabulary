from abc import ABC, abstractmethod


class IRTModel(ABC):
    """
    Abstract base class for different IRT models to calculate the probability of a correct response.
    """

    @abstractmethod
    def probability_of_correct_response(self, skill: float, difficulty: float) -> float:
        pass
