from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from user import User
import random
import os
import json
from datetime import datetime
from lib.gacha_engine import GachaSystem

item_path = os.path.join(os.path.dirname(__file__), "..", "items.json")
item_path = os.path.normpath(item_path)
config_path = os.path.join(os.path.dirname(__file__), "..", "gacha_config.json")
config_path = os.path.normpath(config_path)

gacha = GachaSystem(config_path=config_path)

with open(item_path, "r") as f:
    item_list = json.load(f)

router = APIRouter(prefix="/gacha", tags=["Gacha"])

class History(BaseModel):
    gacha_result: List
    current_pity: int
    current_4star_pity: int
    five_star_rate_on: bool
    four_star_rate_on: bool
    gacha_color: str
    uid: str

three_star_items = []
four_star_items = []
five_star_items = []

for item in item_list:
    if item["rarity"] == "3-star":
        three_star_items.append(item)
    elif item["rarity"] == "4-star":
        four_star_items.append(item)
    elif item["rarity"] == "5-star":
        five_star_items.append(item)

gacha_pool = {
    "3-star": three_star_items,
    "4-star": four_star_items,
    "5-star": five_star_items,
}

