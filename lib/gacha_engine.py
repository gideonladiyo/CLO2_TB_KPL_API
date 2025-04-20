import json
import random
from routers.user import User
from lib.user_lib import UserList
from typing import List, Dict
from datetime import datetime

class GachaSystem:
    def __init__(self, config_path, user_path):
        self.config_path = config_path
        self.config = self.load_config()
        # self.rarity_weights = self.config["rarity_weight"]
        self.rate_up_choices = self.config["rate_up_choices"]
        self.rate_up_weights = self.config["rate_up_weight"]
        self.rarity_choices = self.config["rarity_choices"]
        self.user_list = UserList(config_path=user_path)

    def load_config(self):
        with open(self.config_path, "r") as f:
            return json.load(f)

    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

    def item_return(arr: list):
        return random.choice(arr)

    def reset_percentge(self, updated_4star: int, updated_5star: int, user:dict):
        if updated_5star == 0:
            if user["pity"] >= 70:
                user["rarity_weights"]["3-star"] += 13
                user["rarity_weights"]["5-star"] -= 13
            elif user["pity"] >= 50:
                user["rarity_weights"]["3-star"] += 1
                user["rarity_weights"]["5-star"] -= 1

        if updated_4star == 0:
            if user["four_star_pity"] >= 8:
                user["rarity_weights"]["3-star"] += 30
                user["rarity_weights"]["4-star"] -= 30
            elif user["four_star_pity"] >= 5:
                user["rarity_weights"]["3-star"] += 10
                user["rarity_weights"]["4-star"] -= 10

        self.user_list.save_user_rarity_weight(user["uid"], user["rarity_weights"])

    def change_percentage(self, user: User):
        pity = user["pity"]
        four_star_pity = user["four_star_pity"]
        rarity_weights = user["rarity_weight"]

        # 5 star pity
        if pity == 70:
            rarity_weights["3-star"] -= 12
            rarity_weights["5-star"] += 12
        elif pity == 50:
            rarity_weights["3-star"] -= 1
            rarity_weights["5-star"] += 1

        # 4 star pity
        if four_star_pity == 8:
            rarity_weights["3-star"] -= 20
            rarity_weights["4-star"] += 20
        elif four_star_pity == 5:
            rarity_weights["3-star"] -= 10
            rarity_weights["4-star"] += 10

        self.user_list.save_user_rarity_weight(user["uid"], user["rarity_weights"])

    def determine_status(self, items: List):
        count = {"3-star": 0, "4-star": 0, "5-star": 0}

        for item in items:
            if item["rarity"] in count:
                count[item["rarity"]] += 1

        if count["5-star"] >= 1:
            return "emas"
        elif count["4-star"] >= 1:
            return "ungu"
        else:
            return "biru"

    # gacha system
    def gacha_system(self, rarity: str, user: User, gacha_pool: Dict):
        if rarity != "3-star":
            if rarity == "4-star" and user.four_star_rate_on == False:
                four_star_rateup = random.choices(
                    self.rate_up_choices, weights=self.rate_up_weights, k=1
                )[0]
                if four_star_rateup:
                    item = self.item_return(
                        [item for item in gacha_pool[rarity] if item.is_rate_up]
                    )
                else:
                    item = self.item_return(
                        [item for item in gacha_pool[rarity] if not item.is_rate_up]
                    )
            elif rarity == "4-star" and user.four_star_rate_on == True:
                item = self.item_return([item for item in gacha_pool[rarity] if item.is_rate_up])
            elif rarity == "5-star" and user.is_rate_on == False:
                five_star_rateup = random.choices(
                    self.rate_up_choices, weights=[value for value in self.rate_up_weights], k=1
                )[0]
                if five_star_rateup:
                    item = self.item_return(
                        [item for item in gacha_pool[rarity] if item.is_rate_up]
                    )
                else:
                    item = self.item_return(
                        [item for item in gacha_pool[rarity] if not item.is_rate_up]
                    )
            elif rarity == "5-star" and user.is_rate_on == True:
                item = self.item_return([item for item in gacha_pool[rarity] if item.is_rate_up])
        else:
            item = self.item_return(gacha_pool[rarity])

        self.save_config()

        return item

    # 1 pull
    def gacha(self, user: User, gacha_pool: Dict):
        user.four_star_pity += 1
        user.pity += 1

        self.change_percentage(user)
        if user.four_star_pity == 10:
            rarity = "4-star"
            item = self.gacha_system(rarity, user, gacha_pool)

        elif user.pity == 90:
            rarity = "5-star"
            item = self.gacha_system(rarity, user, gacha_pool)

        else:
            rarity = random.choices(
                self.rarity_choices, weights=[value for value in self.rarity_weights.values()], k=1
            )[0]
            item = self.gacha_system(rarity, user, gacha_pool)

        if item.rarity != "3-star":
            if item.rarity == "4-star":
                if item.is_rate_up:
                    user.four_star_rate_on = False
                else:
                    user.four_star_rate_on = True
                self.reset_percentge(0, user.pity, user)
                user.four_star_pity = 0
            else:
                user.four_star_pity += 1
                if item.is_rate_up:
                    user.is_rate_on = False
                else:
                    user.is_rate_on = True
                self.reset_percentge(user.four_star_pity, 0, user)
                user.pity = 0

        result = {
            "item_name": item.name,
            "rarity": rarity,
            "user_pity": user.pity,
            "user_4star_pity": user.four_star_pity,
            "date": datetime.now(),
        }

        self.save_config()

        return result

    # 10 gacha
    def pull(self, type: str, user: User, gacha_pool: Dict):
        result = {
            "gacha_result": [],
            "current_pity": 0,
            "current_4star_pity": 0,
            "five_star_rateon": False,
            "four_star_rateon": False,
            "gacha_color": "Blue",
            "uid": user.uid,
        }

        if type == "ten_pull":
            for _ in range(10):
                result["gacha_result"].append(self.gacha(user, gacha_pool))
        elif type == "one_pull":
            result["gacha_result"].append(self.gacha(user, gacha_pool))

        result["current_pity"] = user.pity
        result["current_4star_pity"] = user.four_star_pity
        result["five_star_rateon"] = user.is_rate_on
        result["four_star_rateon"] = user.four_star_rate_on
        result["gacha_color"] = self.determine_status(result["gacha_result"])

        self.save_config()

        return result