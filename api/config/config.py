IS_SERVER = True
PREFIX = "/mnt/" if IS_SERVER else "./api/"


class DataConfig:
    PATH_USERS = f"{PREFIX}data/users.csv"
    PATH_ITEMS = f"{PREFIX}data/items.csv"
    PATH_ACHIEVEMENTS = f"{PREFIX}data/achievements.json"
    PATH_RANKS = f"{PREFIX}data/ranks.json"

    PATH_TEST_USERS = f"{PREFIX}/test_data/users.csv"
    PATH_TEST_ITEMS = f"{PREFIX}test_data/items.csv"
    PATH_TEST_ACHIEVEMENTS = f"{PREFIX}test_data/achievements.json"
    PATH_TEST_RANKS = f"{PREFIX}test_data/ranks.json"


class SecurityConfig:
    HTPASSWD_PATH: str = "/mnt/.htpasswd" if IS_SERVER else "./api/middleware/.htpasswd"
    WHITELIST = ["/docs", "/openapi.json", "/docs/oauth2-redirect"]


class ItemCheckConfig:
    SEPERATOR: str = ";"
    LEVENSHTEIN_THRESHOLD: int = 1


class ScoreConfig:
    SCORE_CORRECT: int = 3
    SCORE_MISTAKE: int = 1
    SCORE_WRONG: int = 0
