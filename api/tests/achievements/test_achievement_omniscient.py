import pytest
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from api.core.db.models import UserItem, User, Item
from api.core.achievements.concretes.achievement_omniscient import AchievementOmniscient
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

    # Add multiple items to the database
    for i in range(10):
        item = Item(id=i + 1, question=f"Q{i+1}", solutions=["A"], difficulty=1.0, discrimination=1.0, grade=6)
        session.add(item)

    # Add user items with all correct answers
    for i in range(10):
        user_item = UserItem(user_id=1, item_id=i + 1, correctness=True, timestamp=datetime.now())
        session.add(user_item)

    session.commit()


@pytest.mark.asyncio
async def test_achievement_omniscient(test_session):
    add_test_data(test_session)

    achievement = AchievementOmniscient(test_session)
    assert achievement.unlock_condition(1) is True

    # Add more user items with incorrect answers to ensure the condition fails
    for i in range(10):
        user_item = UserItem(user_id=1, item_id=i + 1, correctness=False, timestamp=datetime.now())
        test_session.add(user_item)

    test_session.commit()

    assert achievement.unlock_condition(1) is True
