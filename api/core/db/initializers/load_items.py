import pandas as pd
from api.core.db.models import Item
import os


def load_items(session, data_path):
    """
    Load or update items from a CSV file into the database based on their id.
    """
    if not os.path.exists(data_path):
        print("Item file does not exist.")
        return

    df = pd.read_csv(data_path)

    try:
        for index, row in df.iterrows():
            # Attempt to find the existing item by id
            item = session.query(Item).filter_by(id=row["id"]).first()
            if item:
                # Update existing item
                item.question = row["question"]
                item.solutions = row["solutions"]
                item.difficulty = row["difficulty"]
                item.discrimination = 1.0
                item.grade = int(row["grade"])
            else:
                # Create new item since it doesn't exist
                item = Item(
                    id=row["id"],
                    question=row["question"],
                    solutions=row["solutions"],
                    difficulty=row["difficulty"],
                    discrimination=1.0,
                    grade=int(row["grade"]),
                )
                session.add(item)

        session.commit()
        print("Items loaded successfully!")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()
