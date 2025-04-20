from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import json
from lib.gacha_engine import GachaSystem
from lib.user_lib import UserList
from lib.file_path import Path
# from datetime import datetime
from models.models import AfterGacha, HistoryGacha


path = Path()
gacha = GachaSystem(config_path=path.config_path, user_path=path.user_path, history_path=path.history_path)
user_list = UserList(user_path=path.user_path, history_path=path.history_path)

with open(path.item_path, "r") as f:
    item_list = json.load(f)

router = APIRouter(prefix="/gacha", tags=["Gacha"])

# class AfterGacha(BaseModel):
#     gacha_result: List
#     current_pity: int
#     current_4star_pity: int
#     five_star_rate_on: bool
#     four_star_rate_on: bool
#     gacha_color: str
#     uid: str

# class HistoryGacha(BaseModel):
#     uid: str
#     item_name: str
#     rarity: str
#     user_pity: int
#     user_4star_pity: int
#     date: datetime

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

@router.get(
    "/history/{uid}",
    response_model=List[HistoryGacha],
    summary="History gacha user berdasarkan UID",
    responses={
        200: {
            "description": {
                "Data history gacha user ditemukan",
            },
            "content": {
                "application/json": {
                    "example": [
                        {"uid": "example_uid", "item_name": "example_item", "rarity": "3-star", "user_pity": 10, "user_4star_pity": 5, "date": "2023-10-01T12:00:00Z"},
                        {"uid": "example_uid", "item_name": "example_item", "rarity": "3-star", "user_pity": 11, "user_4star_pity": 6, "date": "2023-10-01T12:00:00Z"},
                    ]
                }
            }
        }
    }
)
def get_history(uid: str):
    return user_list.get_user_history(uid)

@router.post(
    "/",
    response_model=AfterGacha,
    summary="Melakukan gacha untuk mendapatkan item",
    status_code=201,
    responses={
        201: {
            "description": "Item berhasil didapatkan",
            "content": {
                "gacha_result": [
                    {"uid": "example_uid", "item_name": "example_item", "rarity": "3-star", "user_pity": 10, "user_4star_pity": 5, "date": "2023-10-01T12:00:00Z"}
                ],
                "current_pity": 10,
                "current_4star_pity": 5,
                "five_star_rateon": False,
                "four_star_rateon": False,
                "gacha_color": "Blue",
                "uid": "example UID"
            }
        }
    }
)
def trigger_gacha(uid: str, type: str):
    user = user_list.get_user_by_uid(uid)
    return gacha.pull(type=type, user=user, gacha_pool=gacha_pool)