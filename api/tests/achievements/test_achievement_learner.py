import pytest
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from api.core.db.models import UserItem, User, Item
from api.core.achievements.concretes.achievement_learner import AchievementLearner
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
    user = User(id=1, username="testuser", score=0, ability=0.0, in_control_group=False)
    session.add(user)
    session.commit()

    item = Item(id=1, question="Q1", solutions=["A"], difficulty=1.0, discrimination=1.0, frequency=1, grade=6)
    session.add(item)
    session.commit()

    # Add user items with timestamps for today and previous days
    today = datetime.now()
    for i in range(15):
        timestamp = today - timedelta(minutes=i)
        user_item = UserItem(user_id=1, item_id=i + 1, correctness=True, timestamp=timestamp)
        session.add(user_item)

    for i in range(30):
        timestamp = today - timedelta(days=i + 1)
        user_item = UserItem(user_id=1, item_id=i + 16, correctness=True, timestamp=timestamp)
        session.add(user_item)

    session.commit()


@pytest.mark.asyncio
async def test_achievement_learner(test_session):
    add_test_data(test_session)

    achievement = AchievementLearner(test_session)
    assert achievement.unlock_condition(1) is True

    # Add more user items to ensure the condition fails
    today = datetime.now()
    for i in range(14):
        timestamp = today - timedelta(minutes=i)
        user_item = UserItem(user_id=1, item_id=i + 1, correctness=True, timestamp=timestamp)
        test_session.add(user_item)

    test_session.commit()

    assert achievement.unlock_condition(1) is False
