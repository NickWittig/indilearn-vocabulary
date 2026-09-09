from typing import Tuple
import random


from api.config.config import ItemCheckConfig
from api.core.db.models import Item, User, UserItem
from api.core.db.repository.item_repository import ItemRepository
from api.core.db.repository.user_repository import UserRepository
from api.core.items.item_validator import ItemValidator
from api.core.maths.irt import ItemResponseTheory
from sqlalchemy.orm import Session


class ItemService:
    def __init__(self, session: Session):
        self.repository = ItemRepository(session)
        self.user_repository = UserRepository(session)
        self.irt = ItemResponseTheory()

    def get_item_for_user(self, user: User) -> Tuple[Item | None, str | None]:
        if not user:
            return None, "User not found"

        item: Item = self.get_next_item(user, irt=not (user.in_control_group))

        if not item:
            return None, "No items available"

        return item, None

    def get_next_item(self, user, irt=True):
        if not user:
            return None, "User not found"

        # Step 1: Get all items
        all_items = self.repository.get_all()

        # Step 2: Get the last 100 user items for this user
        last_100_user_items = self.repository.get_n_ui_for(n=100, user_id=user.id)

        # Step 3: Identify items that were answered correctly in the last 100 user items
        correctly_answered_item_ids = {user_item.item_id for user_item in last_100_user_items if user_item.correctness}

        # Step 4: Filter out correctly answered items from all_items
        remaining_items = [item for item in all_items if item.id not in correctly_answered_item_ids]

        if not irt:
            return random.choice(remaining_items) if remaining_items else None

        # Step 5: Calculate probabilities for remaining items
        probabilities = [(item, self.irt.get_probability_of_correct_response(user, item)) for item in remaining_items]

        # Step 6: Further filter items with probability between 0.4 and 0.6
        filtered_items = [(item, prob) for item, prob in probabilities if 0.4 <= prob <= 0.6]

        # Step 7: Select a random item from the filtered list if it's not empty
        if filtered_items:
            selected_item = random.choice(filtered_items)[0]
        else:
            # Select a random item from remaining items if filtered list is empty
            selected_item = random.choice(remaining_items) if remaining_items else None

        return selected_item

    def check_item_solution(self, item_id, user: User, user_solution) -> Tuple[bool | None, str | None]:
        item = self.repository.get_by_id(item_id)

        if not item or not user:
            return None, "Item or User not found"

        is_correct, error_codes = ItemValidator.check_solution(user_solution, item, error_codes=True)

        user_item = UserItem(user_id=user.id, item_id=item_id, correctness=is_correct)
        self.repository.add_user_item(user_item)

        # users, items = self.irt.process_solved_items(self.user_repository.get_all(), self.repository.get_all(), [user_item])
        # self.irt.update_std_values(self.repository.get_all(), self.user_repository.get_all())
        users, items = self.irt.update_user_skill(user, item, user_item)

        self.user_repository.update(user)

        for item in items:
            self.repository.update(item)
        for user in users:
            self.user_repository.update(user)

        return is_correct, error_codes, None

    def get_item_sample_solutions(self, item_id):
        item = self.repository.get_by_id(item_id)

        if not item:
            return None, "Item not found"

        return item.solutions.split(ItemCheckConfig.SEPERATOR)
