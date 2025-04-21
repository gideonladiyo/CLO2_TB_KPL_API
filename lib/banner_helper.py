import json
from fastapi import HTTPException
from lib.file_path import Path

class BannerHelper:
    def __init__(self):
        self.path = Path()
        self.items_path = self.path.item_path
        self.config_path = self.path.banner_config_path
        self.items = self.load_all_items()
        self.config = self.load_item_config()
        self.banners = self.get_all_banners()

    def load_all_items(self):
        try:
            with open(self.items_path, "r") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("Item file must contain list")
                return data
        except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
            print(f"[Error] Failed to load item: {e}")
            return []

    def load_item_config(self):
        print(self.path.banner_config_path)
        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("Item file must contain dict")
                return data
        except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
            print(f"[Error] Failed to load item config: {e}")
            return []

    def get_all_banners(self):
        result = []
        for banner in self.config["banner_list"]:
            three_star_items = []
            four_star_items = []
            five_star_items = []

            for item in self.items:
                item_id = item["id"]
                rarity = item["rarity"]
                
                if rarity == "5-star":
                    if item_id in self.config["rate_off_item_id"]:
                        item_copy = item.copy()
                        five_star_items.append(item_copy)
                    elif item_id == banner["five_star_rate_up_id"]:
                        item_copy = item.copy()
                        item_copy["is_rate_up"] = True
                        five_star_items.append(item_copy)
                
                elif rarity == "4-star":
                    if item_id in banner["four_star_rate_up_id"]:
                        item_copy = item.copy()
                        item_copy["is_rate_up"] = True
                        four_star_items.append(item_copy)
                    else:
                        item_copy = item.copy()
                        four_star_items.append(item_copy)
                
                if rarity == "3-star":
                    item_copy = item.copy()
                    three_star_items.append(item_copy)
                    
            result.append({
                "banner_id": banner["banner_id"],
                "banner_name": banner["banner_name"],
                "gacha_pool": {
                    "3-star": three_star_items,
                    "4-star": four_star_items,
                    "5-star": five_star_items
                }
            })
        return result
    
    def get_banner_by_id(self, banner_id: str):
        for banner in self.banners:
            if banner["banner_id"] == banner_id:
                return banner
        raise HTTPException(status_code=404, detail="Banner tidak ditemukan")