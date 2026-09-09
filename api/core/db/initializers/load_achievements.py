import json
import logging

from api.core.db.models import Achievement

logger = logging.getLogger(__name__)


def load_achievements(session, data_path):
    """
    Load achievements from a JSON file into the database.
    """
    # Load the JSON data
    with open(data_path, "r", encoding="utf-8") as file:
        achievements_data = json.load(file)

    # Insert or update achievements in the database
    try:
        for achievement_data in achievements_data:
            existing_achievement = session.query(Achievement).filter_by(id=achievement_data["id"]).first()
            if existing_achievement:
                # Update existing achievement
                existing_achievement.name_de = achievement_data["name_de"]
                existing_achievement.name_en = achievement_data["name_en"]
                existing_achievement.description_de = achievement_data["description_de"]
                existing_achievement.description_en = achievement_data["description_en"]
                existing_achievement.color = achievement_data["color"]
                existing_achievement.icon_url = achievement_data["icon_url"]
                existing_achievement.class_name = achievement_data["class_name"]
                logger.info(f"Updated achievement with id: {achievement_data['id']}")
            else:
                # Add new achievement
                achievement = Achievement(
                    id=achievement_data["id"],
                    name_de=achievement_data["name_de"],
                    name_en=achievement_data["name_en"],
                    description_de=achievement_data["description_de"],
                    description_en=achievement_data["description_en"],
                    color=achievement_data["color"],
                    icon_url=achievement_data["icon_url"],
                    class_name=achievement_data["class_name"],
                )
                session.add(achievement)
                logger.info(f"Added new achievement with id: {achievement_data['id']}")
        session.commit()
        logger.info("Achievements loaded successfully!")
    except Exception as e:
        logger.error(f"Error loading achievements: {e}", exc_info=True)
        session.rollback()
    finally:
        session.close()
