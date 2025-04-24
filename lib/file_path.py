import os

class Path:
    BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

    CONFIG_PATH = os.path.join(BASE_DIR, "gacha_config.json")
    ITEM_PATH = os.path.join(BASE_DIR, "items.json")
    USER_PATH = os.path.join(BASE_DIR, "users.json")
    HISTORY_PATH = os.path.join(BASE_DIR, "user_history")
    BANNER_CONFIG_PATH = os.path.join(BASE_DIR, "banner_config.json")