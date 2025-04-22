from fastapi import APIRouter
from typing import List
from models.models import Banner
from lib.banner_helper import BannerHelper

router = APIRouter(prefix="/banner", tags=["Banner"])
banner = BannerHelper()

@router.get(
    "/",
    response_model=List[Banner],
    summary="Daftar banner yang tersedia",
    responses={
        200: {
            "description": "Daftar banner yang berhasil diambil",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "banner_id": "B001",
                            "banner_name": "Ganyu's Banner!",
                            "gacha_pool": {
                                "3-star": [],
                                "4-star": [],
                                "5-star": [
                                    {
                                        "id": 1,
                                        "name": "example",
                                        "item_type": "example",
                                        "type": "example",
                                        "rarity": "5-star",
                                        "is_rate_up": False,
                                    }
                                ],
                            },
                        }
                    ]
                }
            },
        }
    },
)
def get_all_banner():
    """
    Mengambil daftar seluruh banner yang tersedia.

    Returns:
    - Daftar objek `Banner` yang berisi informasi tentang banner, termasuk ID, nama banner, dan pool gacha.

    Status Code:
    - **200**: Daftar banner berhasil diambil.
    """
    return banner.get_all_banners()

@router.get(
    "/{banner_id}",
    response_model=Banner,
    summary="Banner berdasarkan ID",
    responses={
        200: {
            "description": "Data banner yang berhasil diambil",
            "content": {
                "application/json": {
                    "example": {
                        "banner_id": "B001",
                        "banner_name": "Ganyu's Banner!",
                        "gacha_pool": {
                            "3-star": [],
                            "4-star": [],
                            "5-star": [
                                {
                                    "id": 1,
                                    "name": "example",
                                    "item_type": "example",
                                    "type": "example",
                                    "rarity": "5-star",
                                    "is_rate_up": False,
                                }
                            ],
                        },
                    }
                }
            },
        },
        404: {
            "description": "Banner dengan ID yang diberikan tidak ditemukan",
            "content": {
                "application/json": {"example": {"detail": "Banner tidak ditemukan"}}
            },
        },
    },
)
def get_banner_by_id(banner_id: str):
    """
    Mengambil informasi banner berdasarkan ID banner.

    Parameter:
    - **banner_id**: ID banner yang akan diambil datanya.

    Returns:
    - Objek `Banner` yang berisi informasi mengenai banner, termasuk nama, ID, dan pool gacha.

    Status Code:
    - **200**: Banner ditemukan dan berhasil diambil.
    - **404**: Banner dengan ID yang diberikan tidak ditemukan.
    """
    return banner.get_banner_by_id(banner_id=banner_id)
