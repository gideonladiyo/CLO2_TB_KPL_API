from fastapi import APIRouter
from typing import List
from lib.gacha_engine import GachaSystem
from lib.user_lib import UserList
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
            "description": "Data history gacha user ditemukan",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "uid": "example_uid",
                            "item_name": "example_item",
                            "rarity": "3-star",
                            "user_pity": 10,
                            "user_4star_pity": 5,
                            "date": "2023-10-01T12:00:00Z",
                        },
                        {
                            "uid": "example_uid",
                            "item_name": "example_item",
                            "rarity": "3-star",
                            "user_pity": 11,
                            "user_4star_pity": 6,
                            "date": "2023-10-01T12:00:00Z",
                        },
                    ]
                }
            },
        },
        404: {
            "description": "User tidak ditemukan",
            "content": {
                "application/json": {"example": {"detail": "User tidak ditemukan"}}
            },
        },
    },
)
def get_history(uid: str):
    """
    Mengambil history gacha pengguna berdasarkan UID.

    Parameter:
    - **uid**: ID pengguna untuk mengambil data history gacha.

    Returns:
    - Daftar objek `HistoryGacha` yang berisi data hasil gacha yang telah dilakukan oleh pengguna.

    Status Code:
    - **200**: History gacha ditemukan.
    - **404**: User dengan UID yang diberikan tidak ditemukan.
    """
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
                "application/json": {
                    "example": {
                        "gacha_result": [
                            {
                                "uid": "example_uid",
                                "item_name": "example_item",
                                "rarity": "3-star",
                                "user_pity": 10,
                                "user_4star_pity": 5,
                                "date": "2023-10-01T12:00:00Z",
                            }
                        ],
                        "current_pity": 10,
                        "current_4star_pity": 5,
                        "five_star_rate_on": False,
                        "four_star_rate_on": False,
                        "gacha_color": "Blue",
                        "uid": "example UID",
                    }
                }
            },
        },
        400: {
            "description": "Bad Request - Invalid pull type or not enough primogems",
            "content": {
                "application/json": {
                    "example": {"detail": "Not enough primogems for a ten pull!"}
                }
            },
        },
    },
)
def trigger_gacha(uid: str, type: str, banner_id: str):
    """
    Men-trigger aksi gacha dengan dua tipe: 'one_pull' atau 'ten_pull'.

    Parameters:
    - **uid**: ID pengguna yang melakukan gacha.
    - **type**: Jenis gacha yang diinginkan ('one_pull' untuk 1x gacha atau 'ten_pull' untuk 10x gacha).
    - **banner_id**: ID banner tempat pengguna melakukan gacha.

    Returns:
    - Respons berupa objek `AfterGacha` yang mencakup:
      - **gacha_result**: Daftar hasil gacha yang didapatkan.
      - **current_pity**: Pity pengguna saat ini untuk item 3-star.
      - **current_4star_pity**: Pity pengguna saat ini untuk item 4-star.
      - **five_star_rate_on**: Status apakah rate 5-star aktif.
      - **four_star_rate_on**: Status apakah rate 4-star aktif.
      - **gacha_color**: Warna dari hasil gacha (misalnya: Blue, Gold).
      - **uid**: ID pengguna yang melakukan gacha.

    Status Code:
    - **201**: Gacha berhasil dan item berhasil didapatkan.
    - **400**: Gagal, primogems tidak cukup untuk tipe pull yang diminta atau tipe pull yang tidak valid.
    """
    return gacha.pull(type=type, uid=uid, banner_id=banner_id)
