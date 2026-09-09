import pytest
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from api.core.db.models import UserItem, User, Item
from api.core.achievements.concretes.achievement_unshakable import AchievementUnshakable
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

    item = Item(id=1, question="Q1", solutions=["A"], difficulty=1.0, discrimination=1.0, grade=6)
    session.add(item)
    session.commit()

    # Add user items with correct answers for the last 7 days
    now = datetime.now()
    for i in range(7):
        for j in range(15):
            timestamp = now - timedelta(days=i)
            user_item = UserItem(user_id=1, item_id=1, correctness=True, timestamp=timestamp)
            session.add(user_item)

    # Add user items with incorrect answers for the last 7 days
    for i in range(7):
        for j in range(5):
            timestamp = now - timedelta(days=i)
            user_item = UserItem(user_id=1, item_id=1, correctness=False, timestamp=timestamp)
            session.add(user_item)

    session.commit()


@pytest.mark.asyncio
async def test_achievement_unshakable(test_session):
    add_test_data(test_session)

    achievement = AchievementUnshakable(test_session)
    assert achievement.unlock_condition(1) is True
