from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import json
from lib.gacha_engine import GachaSystem
from lib.user_lib import UserList
from lib.file_path import Path
# from datetime import datetime
from models.models import AfterGacha, HistoryGacha

gacha = GachaSystem()
user_list = UserList()

router = APIRouter(prefix="/gacha", tags=["Gacha"])

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
                "five_star_rate_on": False,
                "four_star_rateo_n": False,
                "gacha_color": "Blue",
                "uid": "example UID"
            }
        }
    }
)
def trigger_gacha(uid: str, type: str, banner_id: str):
    return gacha.pull(type=type, uid=uid, banner_id=banner_id)