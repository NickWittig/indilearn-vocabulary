import json
import logging
import os


from api.core.db.models import Rank
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def load_ranks(session: Session, data_path):
    """
    Load ranks from a JSON file into the database.
    """
    # Load the JSON data

    if not os.path.exists(data_path):
        print("Item file does not exist.")
        return

    with open(data_path, "r", encoding="utf-8") as file:
        ranks_data = json.load(file)

    # Insert or update ranks in the database

    try:
        for rank_data in ranks_data:
            existing_rank = session.query(Rank).filter_by(id=rank_data["id"]).first()
            if existing_rank:
                # Update existing rank
                existing_rank.name_de = rank_data["name_de"]
                existing_rank.name_en = rank_data["name_en"]
                existing_rank.min_score = rank_data["min_score"]
                existing_rank.max_score = rank_data["max_score"]
                logger.info(f"Updated rank with id: {rank_data['id']}")
            else:
                # Add new rank
                rank = Rank(
                    id=rank_data["id"],
                    name_de=rank_data["name_de"],
                    name_en=rank_data["name_en"],
                    min_score=rank_data["min_score"],
                    max_score=rank_data["max_score"],
                )
                session.add(rank)
                logger.info(f"Added new rank with id: {rank_data['id']}")
        session.commit()
        logger.info("Ranks loaded successfully!")
    except Exception as e:
        logger.error(f"Error loading ranks: {e}", exc_info=True)
        session.rollback()
    finally:
        session.close()
