import os

class Path:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), "..", "gacha_config.json")
        self.item_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "items.json")
        )
        self.user_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "users.json")
        )
        self.history_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "user_history")
        )
        self.banner_config_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "banner_config.json")
        )
