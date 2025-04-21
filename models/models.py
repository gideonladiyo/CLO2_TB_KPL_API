from pydantic import BaseModel
from datetime import datetime
from typing import List


class AfterGacha(BaseModel):
    gacha_result: List
    current_pity: int
    current_4star_pity: int
    five_star_rate_on: bool
    four_star_rate_on: bool
    gacha_color: str
    uid: str

class HistoryGacha(BaseModel):
    uid: str
    item_name: str
    rarity: str
    user_pity: int
    user_4star_pity: int


class User(BaseModel):
    uid: str
    username: str
    password: str
    primogems: int
    pity: int
    four_star_pity: int
    is_rate_on: bool
    four_star_rate_on: bool
    rarity_weight: dict

class PublicUser(BaseModel):
    uid: str
    username: str
    primogems: int
    pity: int
    four_star_pity: int
    is_rate_on: bool
    four_star_rate_on: bool

class UserCreate(BaseModel):
    username: str
    password: str

class Banner(BaseModel):
    banner_id: str
    banner_name: str
    gacha_pool: dict