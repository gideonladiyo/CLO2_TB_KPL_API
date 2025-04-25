import json
import random
from lib.user_lib import UserList
from lib.file_path import Path
from lib.banner_helper import BannerHelper
from typing import List
from fastapi import HTTPException
import os
import time

class GachaSystem:
    def __init__(self):
        self.config_path = Path.CONFIG_PATH

        self.config = self.load_config()
        self.rate_up_choices = self.config["rate_up_choices"]
        self.rate_up_weights = self.config["rate_up_weight"]
        self.rarity_choices = self.config["rarity_choices"]
        self.pity_modifiers = self.config["pity_modifiers"]
        self.four_star_pity_modifiers = self.config["four_star_modifiers"]
        self.reverse_pity_modifiers = self.config["reverse_pity_modifiers"]
        self.reverse_four_star_modifiers = self.config["reverse_four_star_modifiers"]
        self.rarity_status = self.config["rarity_status"]

        self.user_list = UserList()
        self.history_path = Path.HISTORY_PATH
        self.banner_helper = BannerHelper()

    def load_config(self):
        with open(self.config_path, "r", encoding="utf-8") as file:
            raw_config = json.load(file)

        for table_key in ["pity_modifiers", "four_star_modifiers", "reverse_pity_modifiers", "reverse_four_star_modifiers"]:
            raw_config[table_key] = {
                int(k): v for k, v in raw_config[table_key].items()
            }

        raw_config["rarity_status"] = [tuple(pair) for pair in raw_config["rarity_status"]]

        return raw_config

    def save_history(self, uid:str, history_entry: dict):
        history_file = os.path.join(self.history_path, f"{uid}.json")
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                try:
                    history = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
                    print(f"[Error] Failed to load user: {e}")
                    return []
        history.append(history_entry)

        with open(history_file, "w") as f:
            json.dump(history, f, indent=4)

    def item_return(self, arr: list):
        return random.choice(arr)

    def apply_modifiers(self, thresholds: dict, value: int, rarity_weight: dict):
        for threshold in sorted(thresholds.keys(), reverse=True):
            if value >= threshold:
                for rarity, delta in thresholds[threshold].items():
                    rarity_weight[rarity] += delta
                break

    def reset_percentage(self, updated_4star: int, updated_5star: int, user:dict):
        rarity_weight = user["rarity_weight"]
        pity = user["pity"]
        four_star_pity = user["four_star_pity"]

        if updated_5star == 0:
            self.apply_modifiers(self.reverse_pity_modifiers, pity, rarity_weight)

        if updated_4star == 0:
            self.apply_modifiers(self.reverse_four_star_modifiers, four_star_pity, rarity_weight)

        if any(rarity_weight[star] < 0 for star in ["3-star", "4-star", "5-star"]):
            raise HTTPException(status_code=400, detail="rarity weight < 0")

        self.user_list.save_user_rarity_weight(user["uid"], rarity_weight)

    def change_percentage(self, user: dict):
        pity = user["pity"]
        four_star_pity = user["four_star_pity"]
        rarity_weights = user["rarity_weight"]

        if pity in self.pity_modifiers:
            for rarity, delta in self.pity_modifiers[pity].items():
                rarity_weights[rarity] += delta

        if four_star_pity in self.four_star_pity_modifiers:
            for rarity, delta in self.four_star_pity_modifiers[four_star_pity].items():
                rarity_weights[rarity] += delta

        self.user_list.save_user_rarity_weight(user["uid"], user["rarity_weight"])

    def determine_status(self, items: List):
        count = {"3-star": 0, "4-star": 0, "5-star": 0}

        for item in items:
            if item["rarity"] in count:
                count[item["rarity"]] += 1

        for rarity, status in self.rarity_status:
            if count[rarity] >= 1:
                return status

    # gacha system
    def gacha_system(self, rarity: str, user: dict, gacha_pool: dict):
        if rarity != "3-star":
            if rarity == "4-star" and user["four_star_rate_on"] == False:
                four_star_rateup = random.choices(
                    self.rate_up_choices, weights=self.rate_up_weights, k=1
                )[0]
                if four_star_rateup:
                    item = self.item_return(
                        [item for item in gacha_pool[rarity] if item["is_rate_up"]]
                    )
                else:
                    item = self.item_return(
                        [item for item in gacha_pool[rarity] if not item["is_rate_up"]]
                    )
            elif rarity == "4-star" and user["four_star_rate_on"] == True:
                item = self.item_return([item for item in gacha_pool[rarity] if item["is_rate_up"]])
            elif rarity == "5-star" and user["is_rate_on"] == False:
                five_star_rateup = random.choices(
                    self.rate_up_choices, weights=[value for value in self.rate_up_weights], k=1
                )[0]
                if five_star_rateup:
                    item = self.item_return(
                        [item for item in gacha_pool[rarity] if item["is_rate_up"]]
                    )
                else:
                    item = self.item_return(
                        [item for item in gacha_pool[rarity] if not item["is_rate_up"]]
                    )
            elif rarity == "5-star" and user["is_rate_on"] == True:
                item = self.item_return([item for item in gacha_pool[rarity] if item["is_rate_up"]])
        else:
            item = self.item_return(gacha_pool[rarity])

        return item

    # 1 pull
    def gacha(self, user: dict, gacha_pool: dict):
        user["four_star_pity"] += 1
        user["pity"] += 1

        self.change_percentage(user)
        if user["four_star_pity"] == 10:
            rarity = "4-star"
            item = self.gacha_system(rarity, user, gacha_pool)

        elif user["pity"] == 90:
            rarity = "5-star"
            item = self.gacha_system(rarity, user, gacha_pool)

        else:
            rarity = random.choices(
                self.rarity_choices, weights=[value for value in user["rarity_weight"].values()], k=1
            )[0]
            item = self.gacha_system(rarity, user, gacha_pool)

        if item["rarity"] != "3-star":
            if item["rarity"] == "4-star":
                if item["is_rate_up"]:
                    user["four_star_rate_on"] = False
                else:
                    user["four_star_rate_on"] = True
                self.reset_percentage(0, user["pity"], user)
                user["four_star_pity"] = 0
            else:
                user["four_star_pity"] += 1
                if item["is_rate_up"]:
                    user["is_rate_on"] = False
                else:
                    user["is_rate_on"] = True
                self.reset_percentage(user["four_star_pity"], 0, user)
                user["pity"] = 0

        result = {
            "uid": user["uid"],
            "item_name": item["name"],
            "rarity": rarity,
            "user_pity": user["pity"],
            "user_4star_pity": user["four_star_pity"],
        }
        self.save_history(history_entry=result, uid=user["uid"])
        return result

    def pull(self, type: str, uid: str, banner_id: str):
        start = time.time()
        result = {
            "gacha_result": [],
            "current_pity": 0,
            "current_4star_pity": 0,
            "five_star_rate_on": False,
            "four_star_rate_on": False,
            "gacha_color": "Blue",
            "uid": uid,
        }
        gacha_pool = self.banner_helper.get_banner_by_id(banner_id)["gacha_pool"]
        user = self.user_list.get_user_internal(uid)
        if type == "ten_pull":
            if user["primogems"] >= 1600:
                for _ in range(10):
                    result["gacha_result"].append(self.gacha(user, gacha_pool))
                    self.user_list.update_user_primogems(user["uid"])
            else:
                raise HTTPException(status_code=400, detail="Not enough primogems for a ten pull!")
        elif type == "one_pull":
            if user["primogems"] >= 160:
                result["gacha_result"].append(self.gacha(user, gacha_pool))
                self.user_list.update_user_primogems(user["uid"])
            else:
                raise HTTPException(status_code=400, detail="Not enough primogems for a one pull!")
        else:
            raise HTTPException(status_code=400, detail="Invalid pull type specified.")

        result["current_pity"] = user["pity"]
        result["current_4star_pity"] = user["four_star_pity"]
        result["five_star_rate_on"] = user["is_rate_on"]
        result["four_star_rate_on"] = user["four_star_rate_on"]
        result["gacha_color"] = self.determine_status(result["gacha_result"])

        self.user_list.update_user_pity(user=user)
        end = time.time()
        print(f"Waktu eksekusi: {end - start:.4f} detik")

        return result