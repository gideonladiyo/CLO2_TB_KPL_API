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
                                "4-": [],
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
                            "4-": [],
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
        }
    },
)
def get_banner_by_id(banner_id: str):
    return banner.get_banner_by_id(banner_id=banner_id)