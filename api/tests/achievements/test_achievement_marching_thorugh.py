import pytest
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from api.core.db.models import UserItem, User, Item
from api.core.achievements.concretes.achievement_marching_through import AchievementMarchingThrough
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
    # Add test data for users, items, and user items
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


@pytest.mark.asyncio
async def test_achievement_marching_through_fail_with_100_correct(test_session):
    add_test_data(test_session)

    achievement = AchievementMarchingThrough(test_session)
    assert achievement.unlock_condition(1) is False

    # Add more user items with a different timestamp to ensure the condition fails
    for i in range(1, 101):
        user_item = UserItem(user_id=1, item_id=1, correctness=True, timestamp=datetime.now() - timedelta(days=1))
        test_session.add(user_item)
    test_session.commit()

    assert achievement.unlock_condition(1) is False


@pytest.mark.asyncio
async def test_achievement_marching_through_succeed(test_session):

    achievement = AchievementMarchingThrough(test_session)
    assert achievement.unlock_condition(1) is False

    # Add more user items with a different timestamp to ensure the condition fails
    for i in range(1, 101):
        user_item = UserItem(user_id=1, item_id=1, correctness=True, timestamp=datetime.now())
        test_session.add(user_item)
    test_session.commit()

    assert achievement.unlock_condition(1) is True
