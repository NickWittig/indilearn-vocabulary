import pytest
from sqlalchemy.orm import sessionmaker
from api.core.db.models import UserItem, User, Item
from api.core.achievements.concretes.achievement_beyond_the_horizon import AchievementBeyondTheHorizon
from api.core.db.session import Base, engine


@pytest.fixture(scope="module")
def test_session():
    # Create a new database session for testing
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def add_test_data(session):
    # Add test data for users and items
    user = User(id=1, user_name="testuser", password="123", score=0, ability=0.0, rank_id=0, in_control_group=False)
    session.add(user)
    session.commit()

    items = [
        Item(id=1, question="Q1", solutions=["A"], difficulty=1.0, discrimination=1.0, grade=6),
        Item(id=2, question="Q2", solutions=["B"], difficulty=1.0, discrimination=1.0, grade=6),
        # Add more items as needed
    ]
    session.add_all(items)
    session.commit()

    # Add user items with some of the required grade
    for i in range(1, 51):
        user_item = UserItem(user_id=1, item_id=1, correctness=True)
        session.add(user_item)
    session.commit()


@pytest.mark.asyncio
async def test_achievement_beyond_the_horizon(test_session):
    add_test_data(test_session)

    achievement = AchievementBeyondTheHorizon(test_session)
    assert achievement.unlock_condition(1) is False

    # Add more user items to meet the condition
    for i in range(51, 151):
        item = Item(id=i, question=f"Q{i}", solutions=[f"A{i}"], difficulty=1.0, discrimination=1.0, grade=6)
        test_session.add(item)
        user_item = UserItem(user_id=1, item_id=i, correctness=True)
        test_session.add(user_item)
    test_session.commit()

    assert achievement.unlock_condition(1) is True
