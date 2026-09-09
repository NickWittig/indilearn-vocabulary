import logging
import os
import pandas as pd
from api.core.db.models import User

logger = logging.getLogger(__name__)


def load_users(session, data_path):
    """
    Load users from a CSV file into the database.
    """
    if not os.path.exists(data_path):
        print("Item file does not exist.")
        return
    df = pd.read_csv(data_path)

    try:
        for index, row in df.iterrows():
            existing_user = session.query(User).filter_by(user_name=row["user_name"]).first()
            if not existing_user:
                # Add new user
                user = User(
                    id=row["id"],
                    user_name=row["user_name"],
                    score=0,
                    rank_id=0,
                    ability=0,
                    in_control_group=row["in_control_group"],
                )
                session.add(user)
                logger.info(f"Added new user with user_name: {row['user_name']}")
        session.commit()
        logger.info("Users loaded successfully!")
    except Exception as e:
        session.rollback()
        logger.error(f"Error loading users: {e}", exc_info=True)
    finally:
        session.close()
