from fastapi import APIRouter
from typing import List
# from pydantic import BaseModel
from lib.user_lib import UserList
from models.models import User, PublicUser, UserCreate
from lib.file_path import Path

router = APIRouter(prefix="/user", tags=["User"])


# class User(BaseModel):
#     uid: str
#     username: str
#     password: str
#     primogems: int
#     pity: int
#     four_star_pity: int
#     is_rate_on: bool
#     four_star_rate_on: bool
#     rarity_weight: dict


# class PublicUser(BaseModel):
#     uid: str
#     username: str
#     primogems: int
#     pity: int
#     four_star_pity: int
#     is_rate_on: bool
#     four_star_rate_on: bool


# class UserCreate(BaseModel):
#     username: str
#     password: str


path = Path()
user_list = UserList(user_path=path.user_path, history_path=path.history_path)


@router.get(
    "/",
    response_model=List[PublicUser],
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
                            "primogems": 1000000,
                            "pity": 0,
                            "four_star_pity": 0,
                            "is_rate_on": False,
                            "four_star_rate_on": False,
                        },
                        {
                            "uid": "800000002",
                            "username": "Toska",
                            "primogems": 1000000,
                            "pity": 0,
                            "four_star_pity": 0,
                            "is_rate_on": False,
                            "four_star_rate_on": False,
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
    response_model=PublicUser,
    summary="Detail user berdasarkan UID",
    responses={
        200: {
            "description": "Data pelanggan ditemukan",
            "content": {
                "application/json": {
                    "example": {
                        "uid": "800000001",
                        "username": "Gideon",
                        "primogems": 1000000,
                        "pity": 0,
                        "four_star_pity": 0,
                        "is_rate_on": False,
                        "four_star_rate_on": False,
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
    response_model=PublicUser,
    summary="Membuat user baru",
    status_code=201,
    responses={
        201: {
            "description": "User berhasil dibuat",
            "content": {
                "uid": "800000003",
                "username": "Jonathan",
                "primogems": 1000000,
                "pity": 0,
                "four_star_pity": 0,
                "is_rate_on": False,
                "four_star_rate_on": False,
            },
        }
    },
)
def create_user(user: UserCreate):
    return user_list.create_user(user)


@router.put(
    "/{uid}",
    response_model=PublicUser,
    summary="Perbaharui data user",
    responses={
        200: {
            "description": "Data berhasil diperbaharui",
            "content": {
                "application/json": {
                    "example": {
                        "uid": "800000001",
                        "username": "Gideon",
                        "primogems": 1000000,
                        "pity": 0,
                        "four_star_pity": 0,
                        "is_rate_on": False,
                        "four_star_rate_on": False,
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
    responses={
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
