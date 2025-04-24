from fastapi import APIRouter, Body
from typing import List

# from pydantic import BaseModel
from lib.user_lib import UserList
from models.models import PublicUser, UserCreate, User

router = APIRouter(prefix="/user", tags=["User"])

user_list = UserList()

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
    """
    Mengambil seluruh daftar user yang terdaftar dalam sistem.

    Returns:
    - List objek `PublicUser`, yang hanya berisi informasi publik user
      seperti UID, username, primogems, pity, dan status rate-up.

    Status Code:
    - **200 OK**: Berhasil mengambil daftar user.
    """
    return user_list.get_all_user()


@router.get(
    "/{uid}",
    response_model=PublicUser,
    summary="Detail user berdasarkan UID",
    responses={
        200: {
            "description": "Data user berhasil ditemukan",
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
        },
        404: {"description": "User tidak ditemukan"},
    },
)
def get_user(uid: str):
    """
    Mengambil detail informasi publik dari user berdasarkan UID.

    Parameters:
    - **uid** (str): Unique ID dari user yang ingin diambil datanya.

    Returns:
    - Objek `PublicUser` berisi informasi publik user.

    Status Code:
    - **200 OK**: User ditemukan.
    - **404 Not Found**: User tidak ditemukan.
    """
    return user_list.get_public_user_info(uid)

@router.get("/internal/{uid}", include_in_schema=False)
def get_user_internal(uid: str):
    return user_list.get_user_internal(uid)

@router.post(
    "/",
    response_model=PublicUser,
    summary="Membuat user baru",
    status_code=201,
    responses={
        201: {
            "description": "User berhasil dibuat",
            "content": {
                "application/json": {
                    "example": {
                        "uid": "800000003",
                        "username": "Jonathan",
                        "primogems": 1000000,
                        "pity": 0,
                        "four_star_pity": 0,
                        "is_rate_on": False,
                        "four_star_rate_on": False,
                    }
                }
            },
        },
        400: {"description": "Username telah digunakan"},
    },
)
def create_user(user: UserCreate):
    """
    Membuat user baru berdasarkan data yang diberikan.

    Parameters:
    - **user** (UserCreate): Data user baru yang berisi `username` dan `password`.

    Returns:
    - Objek `PublicUser` yang berisi informasi publik user yang berhasil dibuat.

    Status Code:
    - **201 Created**: User berhasil dibuat.
    - **400 Bad Request**: Username sudah digunakan oleh user lain.
    """
    return user_list.create_user(user)

@router.post(
    "/primogems/{uid}",
    response_model=PublicUser,
    summary="Menambah primogems ke user",
    status_code=201,
    responses={
        201: {
            "description": "Primogems berhasil ditambahkan",
            "content": {
                "application/json": {
                    "example": {
                        "uid": "800000003",
                        "username": "Jonathan",
                        "primogems": 1000000,
                        "pity": 0,
                        "four_star_pity": 0,
                        "is_rate_on": False,
                        "four_star_rate_on": False,
                    }
                }
            },
        },
        400: {"description": "Primogems tidak boleh negatif"},
        404: {"description": "User tidak ditemukan"},
    },
)
def add_primogems(uid: str, primogems: int = Body(..., ge=0, description="Jumlah primogems yang ingin ditambahkan")):
    """
    Menambahkan jumlah primogems ke akun user tertentu berdasarkan UID.

    Parameters:
    - **uid** (str): UID dari user (dikirim lewat path).
    - **primogems** (int): Jumlah primogems yang ingin ditambahkan (dikirim lewat body, dan tidak boleh negatif).

    Returns:
    - Objek `PublicUser` yang telah diperbarui.

    Status Code:
    - **201 Created**: Primogems berhasil ditambahkan.
    - **400 Bad Request**: Jika primogems bernilai negatif.
    - **404 Not Found**: Jika user tidak ditemukan.
    """
    user_list.add_user_primogems(uid=uid, primogems=primogems)
    return user_list.get_public_user_info(uid)


@router.post(
    "/auth",
    response_model=User,
    summary="Melakukan authorize",
    status_code=201,
    responses={
        401: {
            "description": "Unauthorized - Username atau password salah",
            "content": {
                "application/json": {
                    "example": {"detail": "Username atau password salah"}
                }
            },
        },
        404: {
            "description": "Not Found - User tidak ditemukan",
            "content": {
                "application/json": {"example": {"detail": "User tidak ditemukan"}}
            },
        },
    },
)
def authorize_user(username: str, password: str):
    user = user_list.user_authentication(username=username, password=password)
    return user


@router.put(
    "/{uid}",
    response_model=PublicUser,
    summary="Perbarui data user",
    responses={
        200: {
            "description": "Data user berhasil diperbarui",
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
        },
        404: {"description": "User tidak ditemukan"},
    },
)
def update_user(uid: str, user: UserCreate):
    """
    Memperbarui data user berdasarkan UID. Hanya `username` dan `password` yang diperbarui;
    atribut lain seperti `primogems`, `pity`, dan lainnya tetap seperti semula.

    Parameters:
    - **uid** (str): UID dari user yang ingin diperbarui.
    - **user** (UserCreate): Objek user baru dengan `username` dan `password` yang diperbarui.

    Returns:
    - Objek `PublicUser` terbaru setelah pembaruan berhasil.

    Status Code:
    - **200 OK**: Jika data user berhasil diperbarui.
    - **404 Not Found**: Jika user dengan UID yang dimaksud tidak ditemukan.
    """
    return user_list.update_user(uid, user)


@router.delete(
    "/{uid}",
    summary="Hapus user berdasarkan UID",
    responses={
        200: {
            "description": "User berhasil dihapus",
            "content": {
                "application/json": {"example": {"message": "User berhasil dihapus"}}
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
    """
    Menghapus user berdasarkan UID.

    Parameters:
    - **uid** (str): UID user yang ingin dihapus.

    Returns:
    - Dictionary berisi pesan konfirmasi penghapusan user.

    Status Code:
    - **200 OK**: User berhasil dihapus.
    - **404 Not Found**: User tidak ditemukan.
    """
    return user_list.delete_user(uid)
