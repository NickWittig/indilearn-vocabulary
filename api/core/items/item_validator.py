import string
from enum import Enum
from typing import List, Union

from api.config.config import ItemCheckConfig
from api.core.db.models import Item
from Levenshtein import distance as levenshtein_distance


class ItemValidationError(Enum):
    CAPITALIZATION_ERROR = "capitalization_error"
    STRIPPING_ERROR = "stripping_error"
    PUNCTUATION_ERROR = "punctuation_error"
    SPELLING_ERROR = "spelling_error"


class ItemValidator:
    @staticmethod
    def check_solution(
        user_solution: str, item: Item, error_codes: bool = False, reverse: bool = False
    ) -> Union[bool, List[ItemValidationError] | None]:
        """Check if the solution is correct and optionally returns error codes.

        Args:
            user_solution (str): The solution given by the user.
            item (Item): The item that is being solved by the user.
            error_codes (bool, optional): Whether to return error codes or not. Defaults to False.
            reverse (bool, optional): Whether to reverse question and solution direction. Defaults to False.

        Returns:
            Union[bool, List[str]]: True if correct, False or list of error codes if not.
        """
        solutions = (
            item.question.split(ItemCheckConfig.SEPERATOR)
            if reverse
            else item.solutions.split(ItemCheckConfig.SEPERATOR)
        )
        cleaned_solutions = [solution.strip() for solution in solutions]

        if ItemValidator.__raw_check(user_solution, cleaned_solutions):
            return True, None

        if not error_codes:
            return False, None

        error_list = []

        if ItemValidator.__capitalization_check(user_solution, cleaned_solutions):
            error_list.append(ItemValidationError.CAPITALIZATION_ERROR)

        if ItemValidator.__stripping_check(user_solution, cleaned_solutions):
            error_list.append(ItemValidationError.STRIPPING_ERROR)

        if ItemValidator.__punctuation_check(user_solution, cleaned_solutions):
            error_list.append(ItemValidationError.PUNCTUATION_ERROR)

        if ItemValidator.__levenshtein_check(user_solution, cleaned_solutions):
            error_list.append(ItemValidationError.SPELLING_ERROR)

        return False, error_list

    @staticmethod
    def __raw_check(user_solution: str, solutions: List[str]) -> bool:
        """Check if the user solution matches any solution exactly.

        Args:
            user_solution (str): The solution given by the user.
            solutions (List[str]): The list of correct solutions.

        Returns:
            bool: True if the solution matches exactly, False otherwise.
        """
        return user_solution in solutions

    @staticmethod
    def __capitalization_check(user_solution: str, solutions: List[str]) -> bool:
        """Check if the user solution matches any solution ignoring capitalization.

        Args:
            user_solution (str): The solution given by the user.
            solutions (List[str]): The list of correct solutions.

        Returns:
            bool: True if the solution matches ignoring capitalization, False otherwise.
        """
        return any(user_solution.lower() == solution.lower() for solution in solutions)

    @staticmethod
    def __stripping_check(user_solution: str, solutions: List[str]) -> bool:
        """Check if the user solution matches any solution after stripping whitespace.

        Args:
            user_solution (str): The solution given by the user.
            solutions (List[str]): The list of correct solutions.

        Returns:
            bool: True if the solution matches after stripping whitespace, False otherwise.
        """
        return any(user_solution.strip() == solution for solution in solutions)

    @staticmethod
    def __punctuation_check(user_solution: str, solutions: List[str]) -> bool:
        """Check if the user solution matches any solution after removing punctuation.

        Args:
            user_solution (str): The solution given by the user.
            solutions (List[str]): The list of correct solutions.

        Returns:
            bool: True if the solution matches after removing punctuation, False otherwise.
        """
        translator = str.maketrans("", "", string.punctuation)
        cleaned_user_solution = user_solution.translate(translator)
        return any(cleaned_user_solution == solution.translate(translator) for solution in solutions)

    @staticmethod
    def __levenshtein_check(user_solution: str, solutions: List[str]) -> bool:
        """Check if the Levenshtein distance between the user solution and any solution is below a threshold.

        Args:
            user_solution (str): The solution given by the user.
            solutions (List[str]): The list of correct solutions.

        Returns:
            bool: True if the Levenshtein distance is below the threshold, False otherwise.
        """
        return any(
            levenshtein_distance(user_solution, solution) <= ItemCheckConfig.LEVENSHTEIN_THRESHOLD
            for solution in solutions
        )
