import os
import json
from lib.file_path import Path

rarity_weight = {"3-star": 94, "4-star": 5, "5-star": 1}

def reset_user_config():
    with open(Path.USER_PATH, "r") as f:
        users = json.load(f)

    for user in users:
        user["primogems"] = 1000000
        user["pity"] = 0
        user["four_star_pity"] = 0
        user["is_rate_on"] = False
        user["four_star_rate_on"] = False
        user["rarity_weight"] = rarity_weight
    
    with open(Path.USER_PATH, "w") as f:
        json.dump(users, f, indent=4)

def reset_history():
    for filename in os.listdir(Path.HISTORY_PATH):
        if filename.endswith(".json"):
            history_dir = os.path.join(Path.HISTORY_PATH, filename)
            if os.path.isfile(history_dir):
                with open(history_dir, "w") as f:
                    json.dump([], f)

def reset_all():
    reset_user_config()
    reset_history()
    return {
        "message": "All user config and history have been reset"
    }