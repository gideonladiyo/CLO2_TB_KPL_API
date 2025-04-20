from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from lib.user_lib import *
import os

router = APIRouter(prefix="/user", tags=["User"])

class User(BaseModel):
    uid: str
    username: str
    password: str
    primogems: int
    pity: int
    four_star_pity: int
    rate_on: bool
    four_star_rate_on: bool
    rarity_weight: dict

class UserCreate(BaseModel):
    username: str
    password: str

config_path = os.path.join(os.path.dirname(__file__), "..", "users.json")
config_path = os.path.normpath(config_path)
user_list = UserList(config_path=config_path)


@router.get(
    "/",
    response_model=List[User],
    summary="Daftar user yang terdaftar",
    responses={
        200: {
            "description": "Daftar user berhasil diambil",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "uid": "800000001",
                            "username": "Gideon",
                            "password": "password123",
                            "primogems": 1000000,
                            "pity": 0,
                            "four_star_pity": 0,
                            "rate_on": False,
                            "four_star_rate_on": False,
                            "rarity_weight": {"3-star": 94, "4-star": 5, "5-star": 1},
                        },
                        {
                            "uid": "800000002",
                            "username": "Toska",
                            "password": "password123",
                            "primogems": 1000000,
                            "pity": 0,
                            "four_star_pity": 0,
                            "rate_on": False,
                            "four_star_rate_on": False,
                            "rarity_weight": {"3-star": 94, "4-star": 5, "5-star": 1},
                        },
                    ]
                }
            },
        }
    },
)
def get_all_user():
    return user_list.get_all_user()


@router.get(
    "/{uid}",
    response_model=User,
    summary="Detail user berdasarkan UID",
    responses={
        200: {
            "description": "Data pelanggan ditemukan",
            "content": {
                "application/json": {
                    "example": {
                        {
                            {
                                "uid": "800000001",
                                "username": "Gideon",
                                "password": "password123",
                                "primogems": 1000000,
                                "pity": 0,
                                "four_star_pity": 0,
                                "rate_on": False,
                                "four_star_rate_on": False,
                                "rarity_weight": {
                                    "3-star": 94,
                                    "4-star": 5,
                                    "5-star": 1,
                                },
                            },
                        }
                    }
                }
            },
        }
    },
)
def get_user(uid: str):
    return user_list.get_user_by_uid(uid)


@router.post(
    "/",
    response_model=User,
    summary="Membuat user baru",
    status_code=201,
    responses={
        201: {
            "description": "User berhasil dibuat",
            "content": {
                {
                    "uid": "800000003",
                    "username": "Jonathan",
                    "password": "password123",
                    "primogems": 1000000,
                    "pity": 0,
                    "four_star_pity": 0,
                    "rate_on": False,
                    "four_star_rate_on": False,
                    "rarity_weight": {"3-star": 94, "4-star": 5, "5-star": 1},
                },
            },
        }
    },
)
def create_user(user: UserCreate):
    return user_list.create_user(user)


@router.put(
    "/{uid}",
    response_model=User,
    summary="Perbaharui data user",
    responses={
        200: {
            "description": "Data berhasil diperbaharui",
            "content": {
                "application/json": {
                    "example": {
                        {
                            "uid": "800000001",
                            "username": "Gideon",
                            "password": "password123",
                            "primogems": 1000000,
                            "pity": 0,
                            "four_star_pity": 0,
                            "rate_on": False,
                            "four_star_rate_on": False,
                            "rarity_weight": {"3-star": 94, "4-star": 5, "5-star": 1},
                        }
                    }
                }
            },
        }
    },
)
def update_user(uid: str, user: UserCreate):
    return user_list.update_user(uid, user)

@router.delete(
    "/{uid}",
    summary="Hapus user berdasarkan UID",
    response={
        200: {
            "description": "User berhasil dihapus",
            "content": {
                "applicatin/json": {"example": {"message": "User berhasil dihapus"}}
            },
        },
        404: {
            "description": "User tidak ditemukan",
            "content": {
                "application/json": {"example": {"message": "User tidak ditemukan"}}
            },
        },
    },
)
def delete_user(uid: str):
    return user_list.delete_user(uid)
